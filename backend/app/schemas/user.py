from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: bool = False
    company_id: Optional[int] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

# Properties to return via API
class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Additional properties to return via API
class UserInDB(User):
    hashed_password: str

# User activity
class UserActivityBase(BaseModel):
    activity_type: str
    description: Optional[str] = None
    ip_address: Optional[str] = None

class UserActivityCreate(UserActivityBase):
    user_id: int

class UserActivity(UserActivityBase):
    id: int
    user_id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True

# User preferences
class UserPreferences(BaseModel):
    default_view: Optional[str] = None
    notification_settings: Optional[dict] = None
    display_settings: Optional[dict] = None
    
    class Config:
        orm_mode = True