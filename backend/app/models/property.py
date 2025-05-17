import uuid
from sqlalchemy import Boolean, Column, String, Integer, Numeric, ForeignKey, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geography

from app.db.session import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = Column(String, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(20), nullable=False)
    property_type = Column(String(50), nullable=False)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Numeric(3, 1), nullable=True)
    square_feet = Column(Integer, nullable=True)
    lot_size = Column(Numeric(10, 2), nullable=True)
    year_built = Column(Integer, nullable=True)
    last_sale_date = Column(Date, nullable=True)
    last_sale_price = Column(Numeric(15, 2), nullable=True)
    current_value = Column(Numeric(15, 2), nullable=True)
    value_estimate_date = Column(Date, nullable=True)
    location = Column(Geography('POINT'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bookmarks = relationship("Bookmark", back_populates="property")
    ownerships = relationship("PropertyOwnership", back_populates="property")
    transactions = relationship("Transaction", back_populates="property")

class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    property = relationship("Property", back_populates="bookmarks")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id", ondelete="CASCADE"))
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String(50), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=True)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("owners.id"), nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    property = relationship("Property", back_populates="transactions")
    seller = relationship("Owner", foreign_keys=[seller_id])
    buyer = relationship("Owner", foreign_keys=[buyer_id])