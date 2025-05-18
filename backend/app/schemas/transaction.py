from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class TransactionBase(BaseModel):
    property_id: UUID
    seller_id: Optional[UUID] = None
    buyer_id: Optional[UUID] = None
    transaction_date: datetime
    transaction_type: str
    amount: float
    description: Optional[str] = None
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    property_id: Optional[UUID] = None
    transaction_date: Optional[datetime] = None
    transaction_type: Optional[str] = None
    amount: Optional[float] = None

class Transaction(TransactionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TransactionWithDetails(Transaction):
    property_address: Optional[str] = None
    seller_name: Optional[str] = None
    buyer_name: Optional[str] = None