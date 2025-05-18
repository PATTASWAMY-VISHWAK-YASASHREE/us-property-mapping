"""
Property mapping model for storing relationships between Zillow property IDs and internal property IDs.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.session import Base

class PropertyMapping(Base):
    """
    Model for mapping external property IDs (like Zillow) to internal property IDs.
    """
    __tablename__ = "property_mappings"
    
    id = Column(String, primary_key=True, index=True)
    internal_property_id = Column(String, ForeignKey("properties.id"), index=True)
    zillow_property_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to the internal property
    property = relationship("Property", back_populates="external_mappings")
    
    def __repr__(self):
        return f"<PropertyMapping(internal_id={self.internal_property_id}, zillow_id={self.zillow_property_id})>"