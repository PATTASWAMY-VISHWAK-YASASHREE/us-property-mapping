from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Float, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.db.base import Base

class WealthData(Base):
    __tablename__ = "wealth_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=False)
    estimated_net_worth = Column(Float, nullable=True)
    income_range = Column(String, nullable=True)
    wealth_tier = Column(String, nullable=True)  # ultra-high, high, affluent, etc.
    liquidity_score = Column(Integer, nullable=True)
    propensity_to_give = Column(Float, nullable=True)
    investment_interests = Column(JSON, nullable=True)
    data_source = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)
    last_updated = Column(DateTime, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("Owner", back_populates="wealth_data")
    
    def __repr__(self):
        return f"<WealthData for Owner {self.owner_id}: {self.wealth_tier}>"