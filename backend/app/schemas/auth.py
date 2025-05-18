from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

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
    logo_url: Optional[str] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    
class UserInvite(BaseModel):
    email: EmailStr
    role: Optional[str] = "user"
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
class UserInviteResponse(BaseModel):
    email: EmailStr
    invitation_id: str
    expires_at: datetime
    detail: str = "Invitation sent successfully"
    
class UserInviteList(BaseModel):
    invites: List[UserInviteResponse]
    
class UserSignup(BaseModel):
    invitation_token: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
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
    
class MFARecoveryCodes(BaseModel):
    codes: List[str]
    
class CSRFToken(BaseModel):
    csrf_token: str