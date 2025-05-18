from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user, get_current_admin_user
from app.core.security import get_password_hash
from app.models.user import User, UserActivity
from app.schemas.user import (
    User as UserSchema,
    UserCreate,
    UserUpdate,
    UserActivity as UserActivitySchema,
    UserPreferences
)

router = APIRouter()

@router.get("/", response_model=List[UserSchema])
def list_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Retrieve users. Admin only.
    """
    # Get users from the same company
    users = db.query(User).filter(User.company_id == current_user.company_id).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Create new user. Admin only.
    """
    # Check if email already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_admin=user_in.is_admin,
        is_active=user_in.is_active,
        company_id=current_user.company_id  # Assign to same company as admin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific user by id.
    """
    # Regular users can only see themselves
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Admin can only see users from same company
    if current_user.is_admin and user.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a user.
    """
    # Regular users can only update themselves
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Admin can only update users from same company
    if current_user.is_admin and user.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update user fields
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    
    # Only admin can change admin status
    if current_user.is_admin and user_in.is_admin is not None:
        user.is_admin = user_in.is_admin
    
    # Update password if provided
    if user_in.password:
        user.hashed_password = get_password_hash(user_in.password)
    
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Delete a user. Admin only.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Admin can only delete users from same company
    if user.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    db.delete(user)
    db.commit()
    
    return None

@router.get("/activity", response_model=List[UserActivitySchema])
def get_user_activity(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get user activity.
    """
    activities = db.query(UserActivity).filter(
        UserActivity.user_id == current_user.id
    ).order_by(UserActivity.timestamp.desc()).offset(skip).limit(limit).all()
    
    return activities

@router.put("/preferences", response_model=UserPreferences)
def update_preferences(
    *,
    db: Session = Depends(get_db),
    preferences: UserPreferences,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update user preferences.
    """
    # In a real implementation, we would store preferences in a separate table
    # but for simplicity we'll just return the input
    
    return preferences