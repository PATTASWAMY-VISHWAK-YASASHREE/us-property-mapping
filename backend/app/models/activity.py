from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.db.base import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    activity_type = Column(String, nullable=False)  # login, search, view, edit, etc.
    entity_type = Column(String, nullable=True)  # property, owner, user, etc.
    entity_id = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="activities")
    
    def __repr__(self):
        return f"<ActivityLog {self.id}: {self.activity_type} by {self.user_id}>"