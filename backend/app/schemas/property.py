from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class PropertyBase(BaseModel):
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    square_feet: Optional[int] = None
    lot_size: Optional[float] = None
    year_built: Optional[int] = None
    last_sale_price: Optional[float] = None
    estimated_value: Optional[float] = None
    owner_id: Optional[int] = None
    additional_data: Optional[Dict[str, Any]] = None

# Properties to receive via API on creation
class PropertyCreate(PropertyBase):
    pass

# Properties to receive via API on update
class PropertyUpdate(PropertyBase):
    pass

# Properties to return via API
class Property(PropertyBase):
    id: int
    last_sale_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Properties for map display
class PropertyMap(BaseModel):
    id: int
    address: str
    property_type: Optional[str] = None
    estimated_value: Optional[float] = None
    latitude: float
    longitude: float
    
    class Config:
        orm_mode = True

# Bookmark schemas
class BookmarkBase(BaseModel):
    property_id: int
    notes: Optional[str] = None

class BookmarkCreate(BookmarkBase):
    pass

class Bookmark(BookmarkBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True