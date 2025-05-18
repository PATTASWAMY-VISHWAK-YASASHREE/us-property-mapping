from typing import Optional
from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None  # Expiration time in seconds
    mfa_required: Optional[bool] = False
    
class RefreshToken(BaseModel):
    refresh_token: str
    
class CompanyRegistration(BaseModel):
    company_name: str
    admin_email: EmailStr
    admin_password: str
    admin_full_name: str
    
class UserInvite(BaseModel):
    email: EmailStr
    role: Optional[str] = "user"
    
class EmailVerification(BaseModel):
    token: str
    
class PasswordReset(BaseModel):
    email: EmailStr
    
class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    
class MFAEnable(BaseModel):
    password: str
    
class MFAVerify(BaseModel):
    token: str

class MFAResponse(BaseModel):
    secret: str
    qr_code: str
    detail: str