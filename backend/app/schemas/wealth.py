from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class WealthDataBase(BaseModel):
    owner_id: UUID
    estimated_net_worth: Optional[float] = None
    income_range: Optional[str] = None
    wealth_tier: Optional[str] = None
    liquidity_score: Optional[int] = None
    propensity_to_give: Optional[float] = None
    investment_interests: Optional[Dict[str, Any]] = None
    data_source: Optional[str] = None
    confidence_score: Optional[float] = None
    last_updated: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class WealthDataCreate(WealthDataBase):
    pass

class WealthDataUpdate(WealthDataBase):
    owner_id: Optional[UUID] = None

class WealthData(WealthDataBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class WealthDataWithOwner(WealthData):
    owner_name: Optional[str] = None
    owner_type: Optional[str] = None