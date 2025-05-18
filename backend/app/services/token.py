from datetime import datetime, timedelta
from typing import Optional, Tuple
import uuid

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, decode_refresh_token
from app.models.token import RefreshToken, TokenBlacklist
from app.models.user import User
from app.schemas.token import TokenResponse

class TokenService:
    @staticmethod
    def create_tokens(user_id: uuid.UUID, db: Session) -> TokenResponse:
        """
        Create access and refresh tokens for a user
        """
        # Create access token with short expiration
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=str(user_id),
            expires_delta=access_token_expires
        )
        
        # Create refresh token with longer expiration
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token, jti = create_refresh_token(
            subject=str(user_id),
            expires_delta=refresh_token_expires
        )
        
        # Store refresh token in database
        db_refresh_token = RefreshToken(
            user_id=user_id,
            token_jti=jti,
            expires_at=datetime.utcnow() + refresh_token_expires
        )
        db.add(db_refresh_token)
        db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
        )
    
    @staticmethod
    def refresh_tokens(refresh_token: str, db: Session) -> Optional[TokenResponse]:
        """
        Create new access and refresh tokens using a valid refresh token
        """
        # Decode and validate the refresh token
        token_data = decode_refresh_token(refresh_token)
        if not token_data or not token_data.jti:
            return None
        
        # Check if token is in database and not revoked
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token_jti == token_data.jti,
            RefreshToken.revoked == False
        ).first()
        
        if not db_token:
            return None
        
        # Check if token has expired
        if db_token.expires_at < datetime.utcnow():
            # Revoke the token
            db_token.revoked = True
            db_token.revoked_at = datetime.utcnow()
            db.commit()
            return None
        
        # Revoke the old token
        db_token.revoked = True
        db_token.revoked_at = datetime.utcnow()
        db.commit()
        
        # Create new tokens
        user_id = uuid.UUID(token_data.sub) if token_data.sub else None
        if not user_id:
            return None
            
        return TokenService.create_tokens(user_id, db)
    
    @staticmethod
    def revoke_token(token_jti: str, token_type: str, db: Session) -> bool:
        """
        Revoke a token by adding it to the blacklist
        """
        # If it's a refresh token, mark it as revoked in the database
        if token_type == "refresh":
            db_token = db.query(RefreshToken).filter(
                RefreshToken.token_jti == token_jti
            ).first()
            
            if db_token:
                db_token.revoked = True
                db_token.revoked_at = datetime.utcnow()
                db.commit()
        
        # Add token to blacklist
        token_blacklist = TokenBlacklist(
            token_jti=token_jti,
            token_type=token_type,
            expires_at=datetime.utcnow() + timedelta(days=1)  # Keep in blacklist for 1 day
        )
        db.add(token_blacklist)
        db.commit()
        
        return True
    
    @staticmethod
    def is_token_blacklisted(token_jti: str, db: Session) -> bool:
        """
        Check if a token is blacklisted
        """
        return db.query(TokenBlacklist).filter(
            TokenBlacklist.token_jti == token_jti
        ).first() is not None
    
    @staticmethod
    def revoke_all_user_tokens(user_id: uuid.UUID, db: Session) -> bool:
        """
        Revoke all refresh tokens for a user
        """
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False
        ).update({"revoked": True, "revoked_at": datetime.utcnow()})
        db.commit()
        return True
    
    @staticmethod
    def cleanup_expired_tokens(db: Session) -> int:
        """
        Remove expired tokens from the database
        """
        now = datetime.utcnow()
        
        # Delete expired blacklisted tokens
        blacklist_deleted = db.query(TokenBlacklist).filter(
            TokenBlacklist.expires_at < now
        ).delete()
        
        # Delete expired refresh tokens
        refresh_deleted = db.query(RefreshToken).filter(
            RefreshToken.expires_at < now
        ).delete()
        
        db.commit()
        return blacklist_deleted + refresh_deleted