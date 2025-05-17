from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

from app.schemas.property import Property

# Shared properties
class OwnerBase(BaseModel):
    name: str
    owner_type: Optional[str] = None
    contact_info: Optional[Dict[str, Any]] = None

# Properties to receive via API on creation
class OwnerCreate(OwnerBase):
    pass

# Properties to receive via API on update
class OwnerUpdate(OwnerBase):
    pass

# Properties to return via API
class Owner(OwnerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Owner with properties
class OwnerWithProperties(Owner):
    properties: List[Property] = []

# Owner wealth data
class OwnerWealthDataBase(BaseModel):
    estimated_net_worth: Optional[float] = None
    income_range: Optional[str] = None
    wealth_tier: Optional[str] = None
    investment_profile: Optional[Dict[str, Any]] = None
    data_sources: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None

class OwnerWealthDataCreate(OwnerWealthDataBase):
    owner_id: int

class OwnerWealthDataUpdate(OwnerWealthDataBase):
    pass

class OwnerWealthData(OwnerWealthDataBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Owner with wealth data
class OwnerWithWealthData(Owner):
    wealth_data: Optional[OwnerWealthData] = None