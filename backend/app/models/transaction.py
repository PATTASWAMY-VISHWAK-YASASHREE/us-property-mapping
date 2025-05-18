from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Float, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=True)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=True)
    transaction_date = Column(DateTime, nullable=False)
    transaction_type = Column(String, nullable=False)  # sale, refinance, etc.
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    source = Column(String, nullable=True)  # data source
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    property = relationship("Property", back_populates="transactions")
    seller = relationship("Owner", foreign_keys=[seller_id], back_populates="sales")
    buyer = relationship("Owner", foreign_keys=[buyer_id], back_populates="purchases")
    
    def __repr__(self):
        return f"<Transaction {self.id}: {self.transaction_type} ${self.amount}>"