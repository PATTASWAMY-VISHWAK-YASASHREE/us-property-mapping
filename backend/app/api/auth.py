from datetime import datetime, timedelta
import logging
import secrets
import pyotp
import qrcode
import io
import base64
import uuid
from typing import Any, Dict, Optional, List

from fastapi import APIRouter, Body, Depends, HTTPException, status, Request, Response, Cookie, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token, get_password_hash, verify_password, 
    generate_mfa_secret, encrypt_sensitive_data, decrypt_sensitive_data,
    decode_token, decode_refresh_token
)
from app.core.dependencies import get_db, get_current_user
from app.models.user import User, Company, ActivityLog
from app.models.token import RefreshToken, TokenBlacklist
from app.models.invitation import Invitation
from app.services.token import TokenService
from app.services.email import EmailService
from app.schemas.auth import (
    Login, TokenResponse, RefreshToken as RefreshTokenSchema, CompanyRegistration, 
    UserInvite, EmailVerification, PasswordReset, 
    PasswordResetConfirm, MFAEnable, MFAVerify, MFAResponse, UserInviteResponse,
    UserSignup
)
from app.schemas.user import UserCreate, User as UserSchema

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Helper function to log security events
def log_security_event(
    db: Session, 
    user_id: Optional[str], 
    activity_type: str, 
    description: str,
    request: Optional[Request] = None,
    success: bool = True
):
    """Log security-related events"""
    try:
        ip_address = None
        user_agent = None
        
        if request:
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent")
        
        log_entry = ActivityLog(
            user_id=user_id,
            activity_type=activity_type,
            description=f"{'SUCCESS' if success else 'FAILED'}: {description}",
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log security event: {e}")

@router.post("/register", response_model=TokenResponse)
def register_company(
    request: Request,
    company_data: CompanyRegistration,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new company and create an admin user.
    """
    # Check if email already exists
    user = db.query(User).filter(User.email == company_data.admin_email).first()
    if user:
        log_security_event(
            db, None, "REGISTRATION", 
            f"Registration attempt with existing email: {company_data.admin_email}",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create company
    company = Company(
        name=company_data.company_name,
        contact_email=company_data.admin_email,
        logo_url=company_data.logo_url,
        address=company_data.address,
        contact_phone=company_data.contact_phone
    )
    db.add(company)
    db.flush()
    
    # Create admin user with hashed password
    user = User(
        email=company_data.admin_email,
        password_hash=get_password_hash(company_data.admin_password),
        first_name=company_data.admin_full_name.split()[0] if company_data.admin_full_name else "",
        last_name=" ".join(company_data.admin_full_name.split()[1:]) if company_data.admin_full_name and len(company_data.admin_full_name.split()) > 1 else "",
        role="admin",
        is_active=True,
        company_id=company.id,
        email_verified=True  # Admin's email is verified by default
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create tokens
    tokens = TokenService.create_tokens(user.id, db)
    
    # Log successful registration
    log_security_event(
        db, str(user.id), "REGISTRATION", 
        f"New company registered: {company_data.company_name}",
        request
    )
    
    return tokens

@router.post("/invite", response_model=UserInviteResponse)
async def invite_user(
    request: Request,
    background_tasks: BackgroundTasks,
    invite_data: UserInvite,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Invite a new user to join the company.
    Only admins can invite users.
    """
    # Check if user is admin
    if current_user.role != "admin":
        log_security_event(
            db, str(current_user.id), "INVITE", 
            f"Non-admin user attempted to invite: {invite_data.email}",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can invite users"
        )
    
    # Check if email already exists as a user
    existing_user = db.query(User).filter(User.email == invite_data.email).first()
    if existing_user:
        log_security_event(
            db, str(current_user.id), "INVITE", 
            f"Invitation attempt for existing user: {invite_data.email}",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if there's already a pending invitation for this email
    existing_invitation = db.query(Invitation).filter(
        Invitation.email == invite_data.email,
        Invitation.company_id == current_user.company_id,
        Invitation.used == False,
        Invitation.expires_at > datetime.utcnow()
    ).first()
    
    if existing_invitation:
        # Return the existing invitation
        return UserInviteResponse(
            email=existing_invitation.email,
            invitation_id=str(existing_invitation.id),
            expires_at=existing_invitation.expires_at,
            detail="Invitation already exists"
        )
    
    # Generate a secure token
    token = secrets.token_urlsafe(32)
    
    # Set expiration date
    expires_at = datetime.utcnow() + timedelta(days=settings.INVITATION_EXPIRE_DAYS)
    
    # Create invitation record
    invitation = Invitation(
        company_id=current_user.company_id,
        email=invite_data.email,
        token=token,
        role=invite_data.role,
        first_name=invite_data.first_name,
        last_name=invite_data.last_name,
        invited_by=current_user.id,
        expires_at=expires_at
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    
    # Get company name
    company = db.query(Company).filter(Company.id == current_user.company_id).first()
    company_name = company.name if company else "Wealth Map"
    
    # Generate invitation link
    invitation_link = f"{settings.FRONTEND_URL}/signup?token={token}"
    
    # Send invitation email in background
    inviter_name = f"{current_user.first_name} {current_user.last_name}".strip()
    if not inviter_name:
        inviter_name = current_user.email
        
    background_tasks.add_task(
        EmailService.send_user_invitation,
        recipient_email=invite_data.email,
        company_name=company_name,
        invitation_link=invitation_link,
        inviter_name=inviter_name
    )
    
    # Log successful invitation
    log_security_event(
        db, str(current_user.id), "INVITE", 
        f"User invited: {invite_data.email} with role {invite_data.role}",
        request
    )
    
    return UserInviteResponse(
        email=invitation.email,
        invitation_id=str(invitation.id),
        expires_at=invitation.expires_at
    )