from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.owner import Owner, OwnerWealthData
from app.models.property import Property
from app.schemas.owner import (
    Owner as OwnerSchema,
    OwnerWithProperties,
    OwnerWealthData as OwnerWealthDataSchema,
    OwnerWithWealthData
)
from app.schemas.property import Property as PropertySchema

router = APIRouter()

@router.get("/", response_model=List[OwnerSchema])
def list_owners(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve owners.
    """
    owners = db.query(Owner).offset(skip).limit(limit).all()
    return owners

@router.get("/{owner_id}", response_model=OwnerWithProperties)
def get_owner(
    owner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific owner by id.
    """
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner not found"
        )
    
    return owner

@router.get("/{owner_id}/wealth", response_model=OwnerWealthDataSchema)
def get_owner_wealth_data(
    owner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get wealth data for a specific owner.
    """
    # Check if owner exists
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner not found"
        )
    
    # Get wealth data
    wealth_data = db.query(OwnerWealthData).filter(OwnerWealthData.owner_id == owner_id).first()
    if not wealth_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wealth data not found for this owner"
        )
    
    return wealth_data

@router.get("/{owner_id}/properties", response_model=List[PropertySchema])
def get_owner_properties(
    owner_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get properties owned by a specific owner.
    """
    # Check if owner exists
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner not found"
        )
    
    # Get properties
    properties = db.query(Property).filter(
        Property.owner_id == owner_id
    ).offset(skip).limit(limit).all()
    
    return properties

@router.get("/search", response_model=List[OwnerWithWealthData])
def search_owners(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    owner_type: Optional[str] = None,
    min_net_worth: Optional[float] = None,
    wealth_tier: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Search owners with various filters.
    """
    # Build query with join to wealth data
    query = db.query(Owner).outerjoin(OwnerWealthData)
    
    # Apply filters
    if q:
        query = query.filter(Owner.name.ilike(f"%{q}%"))
    
    if owner_type:
        query = query.filter(Owner.owner_type == owner_type)
    
    if min_net_worth is not None:
        query = query.filter(OwnerWealthData.estimated_net_worth >= min_net_worth)
    
    if wealth_tier:
        query = query.filter(OwnerWealthData.wealth_tier == wealth_tier)
    
    # Execute query with pagination
    owners = query.offset(skip).limit(limit).all()
    
    # Convert to response model
    result = []
    for owner in owners:
        result.append(
            OwnerWithWealthData(
                id=owner.id,
                name=owner.name,
                owner_type=owner.owner_type,
                contact_info=owner.contact_info,
                created_at=owner.created_at,
                updated_at=owner.updated_at,
                wealth_data=owner.wealth_data
            )
        )
    
    return result