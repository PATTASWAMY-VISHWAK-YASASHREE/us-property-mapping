import uuid
from sqlalchemy import Boolean, Column, String, Integer, Numeric, ForeignKey, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base

class Owner(Base):
    __tablename__ = "owners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    owner_type = Column(String(50), nullable=False)  # individual, company, trust, etc.
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    wealth_data = relationship("WealthData", back_populates="owner", uselist=False)
    property_ownerships = relationship("PropertyOwnership", back_populates="owner")

class PropertyOwnership(Base):
    __tablename__ = "property_ownership"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("owners.id", ondelete="CASCADE"))
    ownership_percentage = Column(Numeric(5, 2), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    property = relationship("Property", back_populates="ownerships")
    owner = relationship("Owner", back_populates="property_ownerships")

class WealthData(Base):
    __tablename__ = "wealth_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("owners.id", ondelete="CASCADE"))
    estimated_net_worth = Column(Numeric(15, 2), nullable=True)
    confidence_level = Column(Integer, nullable=True)  # 1-100 scale
    liquid_assets = Column(Numeric(15, 2), nullable=True)
    real_estate_assets = Column(Numeric(15, 2), nullable=True)
    investment_assets = Column(Numeric(15, 2), nullable=True)
    other_assets = Column(Numeric(15, 2), nullable=True)
    data_source = Column(String(100), nullable=True)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("Owner", back_populates="wealth_data")