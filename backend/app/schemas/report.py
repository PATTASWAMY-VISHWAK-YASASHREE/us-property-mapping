from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class ReportBase(BaseModel):
    name: str
    report_type: str
    parameters: Optional[Dict[str, Any]] = None
    scheduled: Optional[bool] = False
    schedule_frequency: Optional[str] = None

# Properties to receive via API on creation
class ReportCreate(ReportBase):
    pass

# Properties to receive via API on update
class ReportUpdate(ReportBase):
    pass

# Properties to return via API
class Report(ReportBase):
    id: int
    user_id: int
    status: str
    result_data: Optional[Dict[str, Any]] = None
    last_run: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Report template
class ReportTemplate(BaseModel):
    id: str
    name: str
    description: str
    report_type: str
    parameters_schema: Dict[str, Any]