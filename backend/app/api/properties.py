from typing import Any, List, Optional, Dict
import uuid

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.property import Property, Bookmark
from app.models.property_mapping import PropertyMapping
from app.services.zillow_api import ZillowAPIService
from app.schemas.property import (
    Property as PropertySchema,
    PropertyCreate,
    PropertyUpdate,
    PropertyMap,
    Bookmark as BookmarkSchema,
    BookmarkCreate
)

router = APIRouter()

@router.get("/", response_model=List[PropertySchema])
def list_properties(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve properties.
    """
    properties = db.query(Property).offset(skip).limit(limit).all()
    return properties

@router.get("/{property_id}", response_model=PropertySchema)
def get_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific property by id.
    """
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    return property

@router.get("/map", response_model=List[PropertyMap])
def get_properties_for_map(
    db: Session = Depends(get_db),
    lat_min: float = Query(..., description="Minimum latitude"),
    lat_max: float = Query(..., description="Maximum latitude"),
    lng_min: float = Query(..., description="Minimum longitude"),
    lng_max: float = Query(..., description="Maximum longitude"),
    property_type: Optional[str] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get properties for map display within a bounding box.
    """
    # Build query
    query = db.query(Property)
    
    # Filter by bounding box
    # Note: This assumes the location column is a PostGIS POINT geometry
    # In a real implementation, we would use ST_MakeEnvelope and ST_Contains
    # but for simplicity we'll use a placeholder query
    
    # Filter by property type if provided
    if property_type:
        query = query.filter(Property.property_type == property_type)
    
    # Filter by value range if provided
    if min_value is not None:
        query = query.filter(Property.estimated_value >= min_value)
    if max_value is not None:
        query = query.filter(Property.estimated_value <= max_value)
    
    # Limit results for performance
    properties = query.limit(1000).all()
    
    # Convert to map format
    result = []
    for prop in properties:
        # In a real implementation, we would extract coordinates from the geometry
        # but for simplicity we'll use dummy values
        result.append(
            PropertyMap(
                id=prop.id,
                address=prop.address,
                property_type=prop.property_type,
                estimated_value=prop.estimated_value,
                latitude=37.7749,  # Dummy value
                longitude=-122.4194  # Dummy value
            )
        )
    
    return result

@router.get("/search", response_model=List[PropertySchema])
def search_properties(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    property_type: Optional[str] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    min_bedrooms: Optional[int] = None,
    min_bathrooms: Optional[float] = None,
    min_square_feet: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Search properties with various filters.
    """
    # Build query
    query = db.query(Property)
    
    # Apply filters
    if q:
        query = query.filter(
            Property.address.ilike(f"%{q}%") | 
            Property.city.ilike(f"%{q}%") | 
            Property.state.ilike(f"%{q}%") |
            Property.zip_code.ilike(f"%{q}%")
        )
    
    if property_type:
        query = query.filter(Property.property_type == property_type)
    
    if min_value is not None:
        query = query.filter(Property.estimated_value >= min_value)
    
    if max_value is not None:
        query = query.filter(Property.estimated_value <= max_value)
    
    if min_bedrooms is not None:
        query = query.filter(Property.bedrooms >= min_bedrooms)
    
    if min_bathrooms is not None:
        query = query.filter(Property.bathrooms >= min_bathrooms)
    
    if min_square_feet is not None:
        query = query.filter(Property.square_feet >= min_square_feet)
    
    # Execute query with pagination
    properties = query.offset(skip).limit(limit).all()
    
    return properties

@router.get("/bookmarked", response_model=List[PropertySchema])
def get_bookmarked_properties(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get bookmarked properties for the current user.
    """
    # Get property IDs from bookmarks
    bookmarked_property_ids = db.query(Bookmark.property_id).filter(
        Bookmark.user_id == current_user.id
    ).all()
    
    # Extract IDs from result tuples
    property_ids = [id for (id,) in bookmarked_property_ids]
    
    # Get properties
    properties = db.query(Property).filter(
        Property.id.in_(property_ids)
    ).offset(skip).limit(limit).all()
    
    return properties

@router.post("/bookmark", response_model=BookmarkSchema)
def bookmark_property(
    *,
    db: Session = Depends(get_db),
    bookmark_in: BookmarkCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Bookmark a property.
    """
    # Check if property exists
    property = db.query(Property).filter(Property.id == bookmark_in.property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Check if already bookmarked
    existing_bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.property_id == bookmark_in.property_id
    ).first()
    
    if existing_bookmark:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Property already bookmarked"
        )
    
    # Create bookmark
    bookmark = Bookmark(
        user_id=current_user.id,
        property_id=bookmark_in.property_id,
        notes=bookmark_in.notes
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    
    return bookmark

@router.delete("/bookmark/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_bookmark(
    *,
    db: Session = Depends(get_db),
    property_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Remove a property bookmark.
    """
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.property_id == property_id
    ).first()
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    db.delete(bookmark)
    db.commit()
    
    return None

# Zillow API Endpoints

@router.get("/zillow/search", response_model=Dict)
async def zillow_search_property(
    address: str,
    citystatezip: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Search for a property by address using Zillow API.
    """
    zillow_service = ZillowAPIService()
    result = await zillow_service.get_search_results(address, citystatezip)
    
    if not result.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found or error in Zillow API"
        )
    
    return result

@router.get("/zillow/zestimate/{zpid}", response_model=Dict)
async def zillow_get_zestimate(
    zpid: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get Zillow's estimated value for a property.
    """
    zillow_service = ZillowAPIService()
    result = await zillow_service.get_zestimate(zpid)
    
    if not result.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zestimate not found or error in Zillow API"
        )
    
    return result

@router.get("/zillow/comps/{zpid}", response_model=Dict)
async def zillow_get_comps(
    zpid: str,
    count: int = 5,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get comparable properties for a given property.
    """
    zillow_service = ZillowAPIService()
    result = await zillow_service.get_comps(zpid, count)
    
    if not result.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comparable properties not found or error in Zillow API"
        )
    
    return result

@router.get("/zillow/deep-comps/{zpid}", response_model=Dict)
async def zillow_get_deep_comps(
    zpid: str,
    count: int = 5,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get detailed comparable properties for a given property.
    """
    zillow_service = ZillowAPIService()
    result = await zillow_service.get_deep_comps(zpid, count)
    
    if not result.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detailed comparable properties not found or error in Zillow API"
        )
    
    return result

@router.get("/zillow/details/{zpid}", response_model=Dict)
async def zillow_get_property_details(
    zpid: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get enhanced property information.
    """
    zillow_service = ZillowAPIService()
    result = await zillow_service.get_updated_property_details(zpid)
    
    if not result.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property details not found or error in Zillow API"
        )
    
    return result

@router.get("/zillow/demographics/{region_id}", response_model=Dict)
async def zillow_get_demographics(
    region_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get neighborhood demographics information.
    """
    zillow_service = ZillowAPIService()
    result = await zillow_service.get_demographics(region_id)
    
    if not result.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demographics data not found or error in Zillow API"
        )
    
    return result

@router.get("/zillow/region-children/{region_id}", response_model=Dict)
async def zillow_get_region_children(
    region_id: str,
    region_type: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get geographic hierarchy information.
    """
    zillow_service = ZillowAPIService()
    result = await zillow_service.get_region_children(region_id, region_type)
    
    if not result.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region children not found or error in Zillow API"
        )
    
    return result

@router.post("/zillow/save-images", response_model=Dict)
async def save_zillow_property_images(
    *,
    db: Session = Depends(get_db),
    property_id: str = Body(...),
    image_urls: List[str] = Body(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Download and save Zillow property images locally.
    """
    # Check if the property exists
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Save the images
    zillow_service = ZillowAPIService()
    saved_images = await zillow_service.save_property_images(property_id, image_urls)
    
    if not saved_images:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save property images"
        )
    
    return {
        "success": True,
        "saved_images": saved_images
    }

@router.get("/images/{property_id}", response_model=Dict)
async def get_property_images(
    property_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get all images for a property.
    """
    # Check if the property exists
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Import the PropertyImage model
    from app.models.property_image import PropertyImage
    
    # Get all images for the property
    images = db.query(PropertyImage).filter(PropertyImage.property_id == property_id).all()
    
    # Format the response
    image_list = []
    for image in images:
        image_list.append({
            "id": image.id,
            "zillow_url": image.zillow_url,
            "local_path": image.local_path,
            "created_at": image.created_at
        })
    
    return {
        "success": True,
        "property_id": property_id,
        "images": image_list
    }

@router.post("/zillow/map-property", response_model=Dict)
async def map_zillow_to_internal_property(
    *,
    db: Session = Depends(get_db),
    zpid: str = Body(...),
    internal_id: str = Body(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Map a Zillow property ID to an internal property ID.
    """
    # Check if the internal property exists
    property = db.query(Property).filter(Property.id == internal_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Internal property not found"
        )
    
    # Check if mapping already exists
    existing_mapping = db.query(PropertyMapping).filter(
        PropertyMapping.zillow_property_id == zpid
    ).first()
    
    if existing_mapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Zillow property ID is already mapped"
        )
    
    # Create the mapping
    mapping = PropertyMapping(
        id=str(uuid.uuid4()),
        internal_property_id=internal_id,
        zillow_property_id=zpid
    )
    
    db.add(mapping)
    db.commit()
    db.refresh(mapping)
    
    return {
        "success": True,
        "mapping": {
            "id": mapping.id,
            "internal_property_id": mapping.internal_property_id,
            "zillow_property_id": mapping.zillow_property_id,
            "created_at": mapping.created_at
        }
    }