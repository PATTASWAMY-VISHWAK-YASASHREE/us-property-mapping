from datetime import datetime, timedelta
import logging
import secrets
import pyotp
import qrcode
import io
import base64
from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status, Request, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
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
from app.services.token import TokenService
from app.schemas.auth import (
    Login, TokenResponse, RefreshToken as RefreshTokenSchema, CompanyRegistration, 
    UserInvite, EmailVerification, PasswordReset, 
    PasswordResetConfirm, MFAEnable, MFAVerify, MFAResponse
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
        contact_email=company_data.admin_email
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
        company_id=company.id
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

@router.post("/login", response_model=TokenResponse)
def login(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Find user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.password_hash):
        log_security_event(
            db, None, "LOGIN", 
            f"Failed login attempt for email: {form_data.username}",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        log_security_event(
            db, str(user.id), "LOGIN", 
            f"Login attempt for inactive account: {form_data.username}",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    # Check if MFA is enabled
    if user.mfa_enabled:
        # Create a temporary token for MFA verification
        temp_token = create_access_token(
            subject=str(user.id),
            expires_delta=timedelta(minutes=5),
            additional_claims={"mfa_required": True}
        )
        
        log_security_event(
            db, str(user.id), "LOGIN", 
            f"MFA required for user: {user.email}",
            request
        )
        
        # Return a special response indicating MFA is required
        return {
            "access_token": temp_token,
            "token_type": "bearer",
            "mfa_required": True,
            "expires_in": 300  # 5 minutes in seconds
        }
    
    # Update last login time
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Generate tokens
    tokens = TokenService.create_tokens(user.id, db)
    
    # Log successful login
    log_security_event(
        db, str(user.id), "LOGIN", 
        f"Successful login for user: {user.email}",
        request
    )
    
    # Set secure HTTP-only cookie with refresh token
    if settings.HTTPS_ONLY:
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
    
    return tokens

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: Request,
    response: Response,
    token_data: RefreshTokenSchema = Body(...),
    refresh_token_cookie: Optional[str] = Cookie(None, alias="refresh_token"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh access token using a valid refresh token.
    """
    # Use token from cookie if available, otherwise use from request body
    refresh_token = refresh_token_cookie or token_data.refresh_token
    
    if not refresh_token:
        log_security_event(
            db, None, "TOKEN_REFRESH", 
            "Token refresh attempt without refresh token",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required"
        )
    
    # Validate and refresh tokens
    new_tokens = TokenService.refresh_tokens(refresh_token, db)
    
    if not new_tokens:
        log_security_event(
            db, None, "TOKEN_REFRESH", 
            "Invalid refresh token used",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user ID from token
    token_data = decode_refresh_token(refresh_token)
    if token_data and token_data.sub:
        log_security_event(
            db, token_data.sub, "TOKEN_REFRESH", 
            "Successfully refreshed tokens",
            request
        )
    
    # Set secure HTTP-only cookie with new refresh token
    if settings.HTTPS_ONLY:
        response.set_cookie(
            key="refresh_token",
            value=new_tokens.refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
    
    return new_tokens

@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    refresh_token_cookie: Optional[str] = Cookie(None, alias="refresh_token"),
    token: str = Depends(OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Logout user by invalidating tokens.
    """
    try:
        # Decode the access token to get the JTI
        token_data = decode_token(token)
        if token_data:
            # Add access token to blacklist
            TokenService.revoke_token(token_data.jti, "access", db)
        
        # If we have a refresh token in cookie, revoke it
        if refresh_token_cookie:
            refresh_token_data = decode_refresh_token(refresh_token_cookie)
            if refresh_token_data and refresh_token_data.jti:
                TokenService.revoke_token(refresh_token_data.jti, "refresh", db)
        
        # Clear the refresh token cookie
        response.delete_cookie(key="refresh_token", secure=settings.HTTPS_ONLY, httponly=True)
        
        # Log the logout
        log_security_event(
            db, str(current_user.id), "LOGOUT", 
            f"User logged out: {current_user.email}",
            request
        )
        
        return {"detail": "Successfully logged out"}
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        return {"detail": "Successfully logged out"}  # Return success even if there was an error

@router.post("/mfa/enable", response_model=MFAResponse)
def enable_mfa(
    request: Request,
    mfa_data: MFAEnable,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Enable multi-factor authentication.
    """
    # Verify password
    if not verify_password(mfa_data.password, current_user.password_hash):
        log_security_event(
            db, str(current_user.id), "MFA_ENABLE", 
            "Failed MFA enable attempt due to incorrect password",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # Generate a new MFA secret
    mfa_secret = generate_mfa_secret()
    
    # Create a TOTP provider
    totp = pyotp.TOTP(mfa_secret)
    
    # Generate a QR code for the user to scan
    provisioning_uri = totp.provisioning_uri(
        name=current_user.email,
        issuer_name=settings.MFA_ISSUER
    )
    
    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for frontend display
    buffered = io.BytesIO()
    img.save(buffered)
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # Store the encrypted secret in the database
    current_user.mfa_secret = encrypt_sensitive_data(mfa_secret)
    current_user.mfa_enabled = False  # Will be set to true after verification
    db.commit()
    
    log_security_event(
        db, str(current_user.id), "MFA_SETUP", 
        "MFA setup initiated",
        request
    )
    
    return {
        "secret": mfa_secret,
        "qr_code": f"data:image/png;base64,{qr_code_base64}",
        "detail": "Scan the QR code with your authenticator app and verify with the generated code"
    }

@router.post("/mfa/verify")
def verify_mfa(
    request: Request,
    mfa_data: MFAVerify,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Verify MFA token and complete MFA setup.
    """
    # Get the MFA secret
    if not current_user.mfa_secret:
        log_security_event(
            db, str(current_user.id), "MFA_VERIFY", 
            "MFA verification failed - no secret configured",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA not set up for this user"
        )
    
    # Decrypt the secret
    mfa_secret = decrypt_sensitive_data(current_user.mfa_secret)
    
    # Create a TOTP provider
    totp = pyotp.TOTP(mfa_secret)
    
    # Verify the token
    if not totp.verify(mfa_data.token):
        log_security_event(
            db, str(current_user.id), "MFA_VERIFY", 
            "Invalid MFA token provided",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid MFA token"
        )
    
    # Enable MFA for the user
    current_user.mfa_enabled = True
    db.commit()
    
    log_security_event(
        db, str(current_user.id), "MFA_VERIFY", 
        "MFA successfully enabled",
        request
    )
    
    return {"detail": "MFA enabled successfully"}

@router.post("/mfa/login", response_model=TokenResponse)
def mfa_login(
    request: Request,
    response: Response,
    mfa_data: MFAVerify,
    token: str = Depends(OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")),
    db: Session = Depends(get_db)
) -> Any:
    """
    Complete login with MFA verification.
    """
    # Decode the temporary token
    token_data = decode_token(token)
    if not token_data:
        log_security_event(
            db, None, "MFA_LOGIN", 
            "Invalid token for MFA login",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if this is an MFA verification token
    if not token_data.sub or not getattr(token_data, "mfa_required", False):
        log_security_event(
            db, token_data.sub, "MFA_LOGIN", 
            "Token not valid for MFA verification",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type"
        )
    
    # Get the user
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user or not user.is_active or not user.mfa_enabled or not user.mfa_secret:
        log_security_event(
            db, token_data.sub, "MFA_LOGIN", 
            "User not found or MFA not enabled",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found or MFA not enabled"
        )
    
    # Decrypt the secret
    mfa_secret = decrypt_sensitive_data(user.mfa_secret)
    
    # Create a TOTP provider
    totp = pyotp.TOTP(mfa_secret)
    
    # Verify the token
    if not totp.verify(mfa_data.token):
        log_security_event(
            db, str(user.id), "MFA_LOGIN", 
            "Invalid MFA token provided",
            request, False
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid MFA token"
        )
    
    # Update last login time
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Generate tokens
    tokens = TokenService.create_tokens(user.id, db)
    
    # Log successful login
    log_security_event(
        db, str(user.id), "MFA_LOGIN", 
        f"Successful MFA login for user: {user.email}",
        request
    )
    
    # Set secure HTTP-only cookie with refresh token
    if settings.HTTPS_ONLY:
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
    
    return tokens