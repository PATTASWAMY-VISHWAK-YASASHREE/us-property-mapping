from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class SavedSearchBase(BaseModel):
    name: str
    search_parameters: Dict[str, Any]

# Properties to receive via API on creation
class SavedSearchCreate(SavedSearchBase):
    pass

# Properties to receive via API on update
class SavedSearchUpdate(SavedSearchBase):
    pass

# Properties to return via API
class SavedSearch(SavedSearchBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Search request
class SearchRequest(BaseModel):
    query: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"
    page: Optional[int] = 1
    page_size: Optional[int] = 20

# Search suggestion
class SearchSuggestion(BaseModel):
    type: str  # property, owner, address, etc.
    value: str
    display: str