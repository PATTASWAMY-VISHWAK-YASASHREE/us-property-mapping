from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

# System statistics
class SystemStats(BaseModel):
    total_users: int
    active_users: int
    total_properties: int
    total_searches: int
    total_reports: int
    system_health: Dict[str, Any]
    
# Activity log
class ActivityLog(BaseModel):
    id: int
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    activity_type: str
    description: str
    timestamp: datetime
    ip_address: Optional[str] = None
    
    class Config:
        orm_mode = True
        
# System settings
class SystemSettings(BaseModel):
    registration_enabled: bool = True
    maintenance_mode: bool = False
    max_search_results: int = 1000
    default_subscription_tier: str = "free"
    custom_settings: Optional[Dict[str, Any]] = None