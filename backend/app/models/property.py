from sqlalchemy import Boolean, Column, String, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

from app.db.session import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    property_type = Column(String)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    square_feet = Column(Integer)
    lot_size = Column(Float)
    year_built = Column(Integer)
    last_sale_date = Column(DateTime)
    last_sale_price = Column(Float)
    estimated_value = Column(Float)
    location = Column(Geometry('POINT'))
    owner_id = Column(Integer, ForeignKey("owners.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    additional_data = Column(JSON)
    
    # Relationships
    owner = relationship("Owner", back_populates="properties")
    bookmarks = relationship("Bookmark", back_populates="property")

class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    property = relationship("Property", back_populates="bookmarks")