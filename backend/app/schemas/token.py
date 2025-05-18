from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Expiration time in seconds

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None  # "access" or "refresh"

class RefreshTokenPayload(TokenPayload):
    jti: Optional[str] = None  # Unique token identifier for revocation

class TokenBlacklist(BaseModel):
    jti: str
    exp: int  # Expiration time
    created_at: int  # Creation timestamp