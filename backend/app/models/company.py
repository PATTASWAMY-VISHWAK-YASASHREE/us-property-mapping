from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.db.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    settings = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="company")
    
    def __repr__(self):
        return f"<Company {self.name}>"