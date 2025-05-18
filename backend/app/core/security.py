from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union
import secrets
import uuid

from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.token import TokenPayload, RefreshTokenPayload

# Use bcrypt for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a JWT access token with short expiration time
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Base claims
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    
    # Add additional claims if provided
    if additional_claims:
        to_encode.update(additional_claims)
        
    # Encode the JWT
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a refresh token with longer expiration time
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    # Create a unique token ID
    jti = str(uuid.uuid4())
    
    # Create the token payload
    to_encode = {
        "exp": expire, 
        "sub": str(subject), 
        "type": "refresh",
        "jti": jti  # Include a unique ID for token revocation
    }
    
    # Encode the JWT
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, jti

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password for storage
    """
    return pwd_context.hash(password)

def decode_token(token: str) -> Optional[TokenPayload]:
    """
    Decode and validate an access token
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        # Verify it's an access token
        if payload.get("type") != "access":
            return None
            
        token_data = TokenPayload(**payload)
        return token_data
    except (jwt.JWTError, ValidationError):
        return None

def decode_refresh_token(token: str) -> Optional[RefreshTokenPayload]:
    """
    Decode and validate a refresh token
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            return None
            
        token_data = RefreshTokenPayload(**payload)
        return token_data
    except (jwt.JWTError, ValidationError):
        return None

def generate_mfa_secret() -> str:
    """
    Generate a secure secret for MFA
    """
    return secrets.token_hex(20)

def encrypt_sensitive_data(data: str) -> str:
    """
    Encrypt sensitive data for storage
    Note: In a production environment, use a proper encryption library
    """
    # This is a placeholder. In a real implementation, use a proper encryption library
    # like cryptography.fernet
    return f"encrypted:{data}"

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """
    Decrypt sensitive data
    Note: In a production environment, use a proper decryption library
    """
    # This is a placeholder. In a real implementation, use a proper decryption library
    if encrypted_data.startswith("encrypted:"):
        return encrypted_data[10:]
    return encrypted_data