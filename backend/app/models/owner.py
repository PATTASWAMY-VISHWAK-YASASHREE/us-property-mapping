from sqlalchemy import Boolean, Column, String, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_type = Column(String)  # individual, company, trust, etc.
    contact_info = Column(JSON)  # email, phone, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    properties = relationship("Property", back_populates="owner")
    wealth_data = relationship("OwnerWealthData", back_populates="owner", uselist=False)

class OwnerWealthData(Base):
    __tablename__ = "owner_wealth_data"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), unique=True)
    estimated_net_worth = Column(Float)
    income_range = Column(String)
    wealth_tier = Column(String)
    investment_profile = Column(JSON)
    data_sources = Column(JSON)
    confidence_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("Owner", back_populates="wealth_data")