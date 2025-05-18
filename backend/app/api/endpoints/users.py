from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User, UserActivity

router = APIRouter()

@router.get("/me")
def get_current_user():
    """
    Get current user
    """
    return {"email": "user@example.com", "full_name": "Test User"}