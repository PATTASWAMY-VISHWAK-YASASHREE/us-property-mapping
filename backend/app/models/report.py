from sqlalchemy import Boolean, Column, String, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    report_type = Column(String, nullable=False)
    parameters = Column(JSON)
    result_data = Column(JSON)
    status = Column(String, default="pending")  # pending, completed, failed
    scheduled = Column(Boolean, default=False)
    schedule_frequency = Column(String)  # daily, weekly, monthly
    last_run = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reports")