from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.dependencies import get_db, get_current_admin_user
from app.models.user import User, UserActivity
from app.models.property import Property
from app.models.search import SavedSearch
from app.models.report import Report
from app.schemas.admin import SystemStats, ActivityLog, SystemSettings
from app.schemas.user import User as UserSchema

router = APIRouter()

@router.get("/stats", response_model=SystemStats)
def get_system_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Get system statistics. Admin only.
    """
    # Get company ID of current admin
    company_id = current_user.company_id
    
    # Count users in the company
    total_users = db.query(func.count(User.id)).filter(User.company_id == company_id).scalar()
    active_users = db.query(func.count(User.id)).filter(User.company_id == company_id, User.is_active == True).scalar()
    
    # In a real implementation, we would count properties, searches, and reports
    # but for simplicity we'll use dummy values
    total_properties = 1000
    total_searches = 500
    total_reports = 200
    
    return SystemStats(
        total_users=total_users,
        active_users=active_users,
        total_properties=total_properties,
        total_searches=total_searches,
        total_reports=total_reports,
        system_health={
            "database": "healthy",
            "api": "healthy",
            "search_engine": "healthy"
        }
    )

@router.get("/users", response_model=List[UserSchema])
def manage_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Manage users. Admin only.
    """
    # Get users from the same company
    users = db.query(User).filter(User.company_id == current_user.company_id).offset(skip).limit(limit).all()
    return users

@router.get("/activity", response_model=List[ActivityLog])
def view_activity_logs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    activity_type: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    View activity logs. Admin only.
    """
    # Build query
    query = db.query(
        UserActivity.id,
        UserActivity.user_id,
        User.email,
        UserActivity.activity_type,
        UserActivity.description,
        UserActivity.timestamp,
        UserActivity.ip_address
    ).join(User)
    
    # Filter by company
    query = query.filter(User.company_id == current_user.company_id)
    
    # Apply filters if provided
    if user_id:
        query = query.filter(UserActivity.user_id == user_id)
    
    if activity_type:
        query = query.filter(UserActivity.activity_type == activity_type)
    
    # Order by timestamp descending
    query = query.order_by(UserActivity.timestamp.desc())
    
    # Apply pagination
    results = query.offset(skip).limit(limit).all()
    
    # Convert to response model
    activity_logs = []
    for id, user_id, user_email, activity_type, description, timestamp, ip_address in results:
        activity_logs.append(
            ActivityLog(
                id=id,
                user_id=user_id,
                user_email=user_email,
                activity_type=activity_type,
                description=description,
                timestamp=timestamp,
                ip_address=ip_address
            )
        )
    
    return activity_logs

@router.post("/settings", response_model=SystemSettings)
def update_settings(
    *,
    db: Session = Depends(get_db),
    settings_in: SystemSettings,
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Update system settings. Admin only.
    """
    # In a real implementation, we would store settings in the database
    # but for simplicity we'll just return the input
    
    return settings_in