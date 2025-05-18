from typing import Generator, Optional
import uuid
import logging

from fastapi import Depends, HTTPException, status, Request, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_token
from app.db.session import SessionLocal
from app.models.user import User
from app.models.token import TokenBlacklist
from app.schemas.token import TokenPayload

# Configure logging
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_db() -> Generator:
    """
    Database dependency
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def verify_https(request: Request) -> None:
    """
    Verify that the request is using HTTPS in production
    """
    if settings.HTTPS_ONLY and settings.ENVIRONMENT == "production":
        # Check for X-Forwarded-Proto header (common when behind a proxy)
        forwarded_proto = request.headers.get("X-Forwarded-Proto")
        if forwarded_proto and forwarded_proto.lower() != "https":
            logger.warning(f"Non-HTTPS request blocked: {request.url}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="HTTPS required"
            )

def get_token_blacklist_status(token_jti: str, db: Session) -> bool:
    """
    Check if a token is blacklisted
    """
    return db.query(TokenBlacklist).filter(
        TokenBlacklist.token_jti == token_jti
    ).first() is not None

def get_current_user(
    request: Request,
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme),
    user_agent: Optional[str] = Header(None)
) -> User:
    """
    Get the current authenticated user
    """
    # Verify HTTPS
    verify_https(request)
    
    # Decode and validate token
    token_data = decode_token(token)
    if token_data is None:
        logger.warning(f"Invalid token: {token[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if token has a JTI (JWT ID) and if it's blacklisted
    if hasattr(token_data, "jti") and token_data.jti:
        if get_token_blacklist_status(token_data.jti, db):
            logger.warning(f"Blacklisted token used: {token_data.jti}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    # Get user from database
    try:
        user = db.query(User).filter(User.id == uuid.UUID(token_data.sub)).first()
    except (ValueError, TypeError):
        logger.warning(f"Invalid user ID in token: {token_data.sub}")
        raise HTTPException(status_code=404, detail="User not found")
        
    if not user:
        logger.warning(f"User not found: {token_data.sub}")
        raise HTTPException(status_code=404, detail="User not found")
        
    if not user.is_active:
        logger.warning(f"Inactive user attempted access: {user.email}")
        raise HTTPException(status_code=400, detail="Inactive user")
        
    # Log suspicious activity - different user agent
    if user_agent and user.last_user_agent and user_agent != user.last_user_agent:
        logger.warning(f"User agent changed for {user.email}: {user.last_user_agent} -> {user_agent}")
        # In a real app, you might want to trigger additional verification
    
    # Update last user agent
    if user_agent and user_agent != user.last_user_agent:
        user.last_user_agent = user_agent
        db.commit()
        
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current active user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current admin user
    """
    if current_user.role != "admin":
        logger.warning(f"Non-admin user attempted admin action: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user