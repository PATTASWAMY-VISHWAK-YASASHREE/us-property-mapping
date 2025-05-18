import uuid
from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.session import Base

class RefreshToken(Base):
    """
    Model for storing refresh tokens
    """
    __tablename__ = "refresh_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_jti = Column(String(36), unique=True, nullable=False, index=True)  # JWT ID
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Create an index on user_id and revoked for faster lookups
    __table_args__ = (
        Index('ix_refresh_tokens_user_id_revoked', user_id, revoked),
    )

class TokenBlacklist(Base):
    """
    Model for storing blacklisted tokens
    """
    __tablename__ = "token_blacklist"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_jti = Column(String(36), unique=True, nullable=False, index=True)  # JWT ID
    token_type = Column(String(10), nullable=False)  # "access" or "refresh"
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Create an index on expires_at for cleanup jobs
    __table_args__ = (
        Index('ix_token_blacklist_expires_at', expires_at),
    )