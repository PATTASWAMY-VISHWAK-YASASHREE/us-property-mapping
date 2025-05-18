from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.search import SavedSearch
from app.schemas.search import (
    SavedSearch as SavedSearchSchema,
    SavedSearchCreate,
    SavedSearchUpdate,
    SearchRequest,
    SearchSuggestion
)

router = APIRouter()

@router.post("/", response_model=Dict)
def perform_search(
    *,
    db: Session = Depends(get_db),
    search_request: SearchRequest,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Perform a search across properties and owners.
    """
    # In a real implementation, we would perform a search across multiple entities
    # but for simplicity we'll just return a dummy response
    
    return {
        "total": 42,
        "page": search_request.page,
        "page_size": search_request.page_size,
        "results": [
            {
                "type": "property",
                "id": 1,
                "address": "123 Main St",
                "estimated_value": 500000
            },
            {
                "type": "owner",
                "id": 1,
                "name": "John Doe",
                "properties_count": 3
            }
        ]
    }

@router.get("/saved", response_model=List[SavedSearchSchema])
def get_saved_searches(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get saved searches for the current user.
    """
    saved_searches = db.query(SavedSearch).filter(
        SavedSearch.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return saved_searches

@router.post("/save", response_model=SavedSearchSchema)
def save_search(
    *,
    db: Session = Depends(get_db),
    search_in: SavedSearchCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Save a search.
    """
    saved_search = SavedSearch(
        user_id=current_user.id,
        name=search_in.name,
        search_parameters=search_in.search_parameters
    )
    db.add(saved_search)
    db.commit()
    db.refresh(saved_search)
    
    return saved_search

@router.delete("/{search_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_search(
    *,
    db: Session = Depends(get_db),
    search_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete a saved search.
    """
    saved_search = db.query(SavedSearch).filter(
        SavedSearch.id == search_id,
        SavedSearch.user_id == current_user.id
    ).first()
    
    if not saved_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved search not found"
        )
    
    db.delete(saved_search)
    db.commit()
    
    return None

@router.get("/suggestions", response_model=List[SearchSuggestion])
def get_search_suggestions(
    db: Session = Depends(get_db),
    q: str = Query(..., min_length=2),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get search suggestions based on input.
    """
    # In a real implementation, we would query the database for suggestions
    # but for simplicity we'll just return dummy data
    
    suggestions = [
        SearchSuggestion(
            type="property",
            value="123 Main St",
            display="123 Main St, San Francisco, CA"
        ),
        SearchSuggestion(
            type="owner",
            value="John Doe",
            display="John Doe (3 properties)"
        ),
        SearchSuggestion(
            type="address",
            value="Market Street",
            display="Market Street, San Francisco, CA"
        )
    ]
    
    return suggestions