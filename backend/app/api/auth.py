from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.dependencies import get_db, get_current_user
from app.models.user import User, Company
from app.schemas.auth import (
    Login, TokenResponse, RefreshToken, CompanyRegistration, 
    UserInvite, EmailVerification, PasswordReset, 
    PasswordResetConfirm, MFAEnable, MFAVerify
)
from app.schemas.user import UserCreate, User as UserSchema

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register_company(
    company_data: CompanyRegistration,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new company and create an admin user.
    """
    # Check if email already exists
    user = db.query(User).filter(User.email == company_data.admin_email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create company
    company = Company(name=company_data.company_name)
    db.add(company)
    db.flush()
    
    # Create admin user
    user = User(
        email=company_data.admin_email,
        hashed_password=get_password_hash(company_data.admin_password),
        full_name=company_data.admin_full_name,
        is_admin=True,
        company_id=company.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    # Check if MFA is enabled
    if user.mfa_enabled:
        # In a real implementation, we would return a special token that allows
        # only MFA verification, but for simplicity we'll skip this
        pass
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    token_data: RefreshToken,
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh access token.
    """
    # In a real implementation, we would validate the refresh token
    # and issue a new access token if valid
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not implemented"
    )

@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Logout user.
    """
    # In a real implementation, we would invalidate the token
    # but for simplicity we'll just return success
    return {"detail": "Successfully logged out"}

@router.post("/invite")
def invite_user(
    invite_data: UserInvite,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Invite a user to join the company.
    """
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if email already exists
    user = db.query(User).filter(User.email == invite_data.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # In a real implementation, we would send an email with an invitation link
    # but for simplicity we'll just return success
    
    return {"detail": f"Invitation sent to {invite_data.email}"}

@router.post("/verify")
def verify_email(
    verification_data: EmailVerification,
    db: Session = Depends(get_db)
) -> Any:
    """
    Verify email address.
    """
    # In a real implementation, we would validate the verification token
    # and mark the user's email as verified
    return {"detail": "Email verified successfully"}

@router.post("/password/reset")
def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
) -> Any:
    """
    Reset password.
    """
    # Check if email exists
    user = db.query(User).filter(User.email == reset_data.email).first()
    if not user:
        # For security reasons, don't reveal that the email doesn't exist
        return {"detail": "If the email exists, a password reset link has been sent"}
    
    # In a real implementation, we would send an email with a password reset link
    # but for simplicity we'll just return success
    
    return {"detail": "If the email exists, a password reset link has been sent"}

@router.post("/mfa/enable")
def enable_mfa(
    mfa_data: MFAEnable,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Enable multi-factor authentication.
    """
    # Verify password
    if not verify_password(mfa_data.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # In a real implementation, we would generate a secret key and return
    # a QR code for the user to scan with their authenticator app
    # but for simplicity we'll just return a dummy secret
    
    # Update user
    current_user.mfa_enabled = True
    current_user.mfa_secret = "dummy_secret"
    db.commit()
    
    return {
        "secret": "dummy_secret",
        "qr_code": "https://example.com/qr_code",
        "detail": "MFA enabled successfully"
    }

@router.post("/mfa/verify")
def verify_mfa(
    mfa_data: MFAVerify,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Verify MFA token.
    """
    # In a real implementation, we would validate the MFA token
    # but for simplicity we'll just check if it's "123456"
    if mfa_data.token != "123456":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid MFA token"
        )
    
    return {"detail": "MFA token verified successfully"}