"""
Model for storing property images downloaded from Zillow API.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.base import Base

class PropertyImage(Base):
    """
    Model for storing property images downloaded from Zillow API.
    """
    __tablename__ = "property_images"
    
    id = Column(String, primary_key=True, index=True)
    property_id = Column(String, ForeignKey("properties.id"), index=True)
    zillow_url = Column(String, nullable=False)
    local_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to the property
    property = relationship("Property", back_populates="images")