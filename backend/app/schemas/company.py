from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl

class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    name: Optional[str] = None

class Company(CompanyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CompanyWithUsers(Company):
    users: List["UserBase"] = []

# To avoid circular imports
from app.schemas.user import UserBase
CompanyWithUsers.update_forward_refs()