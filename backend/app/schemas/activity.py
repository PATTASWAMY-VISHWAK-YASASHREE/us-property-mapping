from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class ActivityLogBase(BaseModel):
    user_id: UUID
    activity_type: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    description: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class ActivityLogCreate(ActivityLogBase):
    pass

class ActivityLog(ActivityLogBase):
    id: UUID
    timestamp: datetime

    class Config:
        orm_mode = True

class ActivityLogWithUser(ActivityLog):
    user_email: Optional[str] = None
    user_name: Optional[str] = None