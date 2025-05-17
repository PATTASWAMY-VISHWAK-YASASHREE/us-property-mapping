"""
Zillow API Service for property data integration via RapidAPI.
"""
import os
import time
import json
import logging
from typing import Dict, List, Optional, Any, Union
import httpx
from functools import lru_cache
from datetime import datetime, timedelta

from ..core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class ZillowAPIException(Exception):
    """Exception raised for Zillow API errors."""
    pass

class ZillowAPIRateLimitException(ZillowAPIException):
    """Exception raised when Zillow API rate limit is exceeded."""
    pass

class ZillowAPIService:
    """
    Service for interacting with the Zillow API via RapidAPI.
    
    This service handles:
    - API authentication
    - Request formatting
    - Response parsing
    - Error handling
    - Rate limiting
    - Caching
    - Request queuing
    """
    
    BASE_URL = "https://zillow-com1.p.rapidapi.com"
    CACHE_EXPIRY = settings.ZILLOW_CACHE_EXPIRY
    MAX_RETRIES = settings.ZILLOW_MAX_RETRIES
    RETRY_DELAY = settings.ZILLOW_RETRY_DELAY
    
    def __init__(self):
        """Initialize the Zillow API service."""
        self.api_key = os.environ.get("RAPIDAPI_KEY", settings.RAPIDAPI_KEY)
        if not self.api_key:
            logger.warning("RAPIDAPI_KEY environment variable not set")
        
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": settings.ZILLOW_API_HOST
        }
        
        # Initialize cache
        self._cache = {}
        self._request_queue = []
        
    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the Zillow API with retry logic and error handling.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters for the request
            
        Returns:
            Parsed JSON response
            
        Raises:
            ZillowAPIException: If the API request fails
            ZillowAPIRateLimitException: If rate limit is exceeded
        """
        url = f"{self.BASE_URL}{endpoint}"
        cache_key = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        
        # Check cache first
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            logger.debug(f"Cache hit for {cache_key}")
            return cached_result
        
        # Make the request with retries
        retries = 0
        while retries <= self.MAX_RETRIES:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=self.headers, params=params)
                    
                if response.status_code == 429:
                    # Rate limit exceeded
                    retries += 1
                    if retries <= self.MAX_RETRIES:
                        wait_time = self.RETRY_DELAY * (2 ** (retries - 1))  # Exponential backoff
                        logger.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise ZillowAPIRateLimitException("Rate limit exceeded and max retries reached")
                
                response.raise_for_status()
                data = response.json()
                
                # Cache the successful response
                self._add_to_cache(cache_key, data)
                return data
                
            except httpx.HTTPStatusError as e:
                retries += 1
                if retries <= self.MAX_RETRIES:
                    logger.warning(f"HTTP error {e}. Retrying {retries}/{self.MAX_RETRIES}...")
                    time.sleep(self.RETRY_DELAY)
                else:
                    logger.error(f"HTTP error after {self.MAX_RETRIES} retries: {e}")
                    raise ZillowAPIException(f"HTTP error: {e}")
            
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise ZillowAPIException(f"Unexpected error: {e}")
    
    def _get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Get a response from the cache if it exists and is not expired."""
        if key in self._cache:
            entry = self._cache[key]
            if datetime.now() < entry["expires"]:
                return entry["data"]
            else:
                # Remove expired entry
                del self._cache[key]
        return None
    
    def _add_to_cache(self, key: str, data: Dict[str, Any]) -> None:
        """Add a response to the cache with expiration time."""
        self._cache[key] = {
            "data": data,
            "expires": datetime.now() + timedelta(seconds=self.CACHE_EXPIRY)
        }
        
    def _queue_request(self, endpoint: str, params: Dict[str, Any]) -> None:
        """Add a request to the queue for batch processing."""
        self._request_queue.append({"endpoint": endpoint, "params": params})
        
    async def process_queue(self) -> List[Dict[str, Any]]:
        """Process all requests in the queue and return results."""
        results = []
        queue_copy = self._request_queue.copy()
        self._request_queue = []
        
        for request in queue_copy:
            try:
                result = await self._make_request(request["endpoint"], request["params"])
                results.append({"success": True, "data": result, "request": request})
            except Exception as e:
                results.append({"success": False, "error": str(e), "request": request})
                
        return results
    
    # Core Zillow API Endpoints
    
    async def get_search_results(self, address: str, citystatezip: str) -> Dict[str, Any]:
        """
        Get property details by address using Zillow's GetSearchResults API.
        
        Args:
            address: Street address of the property
            citystatezip: City, state, and ZIP code
            
        Returns:
            Property details including Zillow property ID (zpid)
        """
        endpoint = "/GetSearchResults"
        params = {
            "address": address,
            "citystatezip": citystatezip
        }
        
        response = await self._make_request(endpoint, params)
        return self._transform_search_results(response)
    
    async def get_zestimate(self, zpid: str) -> Dict[str, Any]:
        """
        Get Zillow's estimated value for a property.
        
        Args:
            zpid: Zillow property ID
            
        Returns:
            Property valuation data
        """
        endpoint = "/GetZestimate"
        params = {"zpid": zpid}
        
        response = await self._make_request(endpoint, params)
        return self._transform_zestimate(response)
    
    async def get_comps(self, zpid: str, count: int = 5) -> Dict[str, Any]:
        """
        Get comparable properties for a given property.
        
        Args:
            zpid: Zillow property ID
            count: Number of comparable properties to return
            
        Returns:
            List of comparable properties
        """
        endpoint = "/GetComps"
        params = {
            "zpid": zpid,
            "count": count
        }
        
        response = await self._make_request(endpoint, params)
        return self._transform_comps(response)
    
    async def get_deep_comps(self, zpid: str, count: int = 5) -> Dict[str, Any]:
        """
        Get detailed comparable properties for a given property.
        
        Args:
            zpid: Zillow property ID
            count: Number of comparable properties to return
            
        Returns:
            List of comparable properties with detailed information
        """
        endpoint = "/GetDeepComps"
        params = {
            "zpid": zpid,
            "count": count
        }
        
        response = await self._make_request(endpoint, params)
        return self._transform_deep_comps(response)
    
    async def get_updated_property_details(self, zpid: str) -> Dict[str, Any]:
        """
        Get enhanced property information.
        
        Args:
            zpid: Zillow property ID
            
        Returns:
            Detailed property information
        """
        endpoint = "/GetUpdatedPropertyDetails"
        params = {"zpid": zpid}
        
        response = await self._make_request(endpoint, params)
        return self._transform_property_details(response)
    
    async def get_demographics(self, region_id: str) -> Dict[str, Any]:
        """
        Get neighborhood demographics information.
        
        Args:
            region_id: Zillow region ID
            
        Returns:
            Demographic data for the region
        """
        endpoint = "/GetDemographics"
        params = {"regionid": region_id}
        
        response = await self._make_request(endpoint, params)
        return self._transform_demographics(response)
    
    async def get_region_children(self, region_id: str, region_type: str) -> Dict[str, Any]:
        """
        Get geographic hierarchy information.
        
        Args:
            region_id: Zillow region ID
            region_type: Type of region (e.g., "neighborhood", "city", "county")
            
        Returns:
            Child regions within the specified region
        """
        endpoint = "/GetRegionChildren"
        params = {
            "regionid": region_id,
            "regiontype": region_type
        }
        
        response = await self._make_request(endpoint, params)
        return self._transform_region_children(response)
    
    # Data transformation methods
    
    def _transform_search_results(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Zillow search results to standardized format."""
        try:
            result = response.get("searchresults", {}).get("response", {})
            if not result:
                return {"success": False, "message": "No results found"}
                
            # Extract the property data
            property_data = result.get("results", {}).get("result", [])
            if not isinstance(property_data, list):
                property_data = [property_data]
                
            transformed = {
                "success": True,
                "properties": []
            }
            
            for prop in property_data:
                transformed["properties"].append({
                    "zpid": prop.get("zpid", ""),
                    "address": {
                        "street": prop.get("address", {}).get("street", ""),
                        "city": prop.get("address", {}).get("city", ""),
                        "state": prop.get("address", {}).get("state", ""),
                        "zipcode": prop.get("address", {}).get("zipcode", ""),
                        "latitude": prop.get("address", {}).get("latitude", ""),
                        "longitude": prop.get("address", {}).get("longitude", "")
                    },
                    "links": {
                        "home_details": prop.get("links", {}).get("homedetails", ""),
                        "maps": prop.get("links", {}).get("mapthishome", ""),
                        "comparables": prop.get("links", {}).get("comparables", "")
                    }
                })
                
            return transformed
        except Exception as e:
            logger.error(f"Error transforming search results: {e}")
            return {"success": False, "message": f"Error transforming data: {str(e)}"}
    
    def _transform_zestimate(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Zillow Zestimate data to standardized format."""
        try:
            result = response.get("zestimate", {}).get("response", {})
            if not result:
                return {"success": False, "message": "No Zestimate found"}
                
            zestimate = result.get("zestimate", {})
            
            return {
                "success": True,
                "zpid": result.get("zpid", ""),
                "zestimate": {
                    "amount": zestimate.get("amount", {}).get("value", ""),
                    "currency": zestimate.get("amount", {}).get("currency", "USD"),
                    "last_updated": zestimate.get("last_updated", ""),
                    "value_change": zestimate.get("valueChange", {}).get("value", ""),
                    "valuation_range": {
                        "low": zestimate.get("valuationRange", {}).get("low", {}).get("value", ""),
                        "high": zestimate.get("valuationRange", {}).get("high", {}).get("value", "")
                    },
                    "percentile": zestimate.get("percentile", "")
                }
            }
        except Exception as e:
            logger.error(f"Error transforming Zestimate: {e}")
            return {"success": False, "message": f"Error transforming data: {str(e)}"}
    
    def _transform_comps(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Zillow comparable properties data to standardized format."""
        try:
            result = response.get("comps", {}).get("response", {})
            if not result:
                return {"success": False, "message": "No comparable properties found"}
                
            principal = result.get("properties", {}).get("principal", {})
            comps = result.get("properties", {}).get("comparables", {}).get("comp", [])
            
            if not isinstance(comps, list):
                comps = [comps]
                
            transformed = {
                "success": True,
                "principal": {
                    "zpid": principal.get("zpid", ""),
                    "address": principal.get("address", {}).get("street", ""),
                    "zestimate": principal.get("zestimate", {}).get("amount", {}).get("value", "")
                },
                "comparables": []
            }
            
            for comp in comps:
                transformed["comparables"].append({
                    "zpid": comp.get("zpid", ""),
                    "address": comp.get("address", {}).get("street", ""),
                    "zestimate": comp.get("zestimate", {}).get("amount", {}).get("value", ""),
                    "similarity_score": comp.get("score", "")
                })
                
            return transformed
        except Exception as e:
            logger.error(f"Error transforming comps: {e}")
            return {"success": False, "message": f"Error transforming data: {str(e)}"}
    
    def _transform_deep_comps(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Zillow detailed comparable properties data to standardized format."""
        try:
            result = response.get("deepcomps", {}).get("response", {})
            if not result:
                return {"success": False, "message": "No deep comparable properties found"}
                
            principal = result.get("properties", {}).get("principal", {})
            comps = result.get("properties", {}).get("comparables", {}).get("comp", [])
            
            if not isinstance(comps, list):
                comps = [comps]
                
            transformed = {
                "success": True,
                "principal": self._extract_property_details(principal),
                "comparables": []
            }
            
            for comp in comps:
                comp_data = self._extract_property_details(comp)
                comp_data["similarity_score"] = comp.get("score", "")
                transformed["comparables"].append(comp_data)
                
            return transformed
        except Exception as e:
            logger.error(f"Error transforming deep comps: {e}")
            return {"success": False, "message": f"Error transforming data: {str(e)}"}
    
    def _transform_property_details(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Zillow property details to standardized format."""
        try:
            result = response.get("updatedPropertyDetails", {}).get("response", {})
            if not result:
                return {"success": False, "message": "No property details found"}
                
            return {
                "success": True,
                "zpid": result.get("zpid", ""),
                "address": {
                    "street": result.get("address", {}).get("street", ""),
                    "city": result.get("address", {}).get("city", ""),
                    "state": result.get("address", {}).get("state", ""),
                    "zipcode": result.get("address", {}).get("zipcode", ""),
                    "latitude": result.get("address", {}).get("latitude", ""),
                    "longitude": result.get("address", {}).get("longitude", "")
                },
                "property_type": result.get("editedFacts", {}).get("useCode", ""),
                "year_built": result.get("editedFacts", {}).get("yearBuilt", ""),
                "lot_size": result.get("editedFacts", {}).get("lotSizeSqFt", ""),
                "finished_size": result.get("editedFacts", {}).get("finishedSqFt", ""),
                "bedrooms": result.get("editedFacts", {}).get("bedrooms", ""),
                "bathrooms": result.get("editedFacts", {}).get("bathrooms", ""),
                "total_rooms": result.get("editedFacts", {}).get("totalRooms", ""),
                "images": result.get("images", {}).get("image", {}).get("url", []),
                "last_updated": result.get("lastUpdated", "")
            }
        except Exception as e:
            logger.error(f"Error transforming property details: {e}")
            return {"success": False, "message": f"Error transforming data: {str(e)}"}
    
    def _transform_demographics(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Zillow demographics data to standardized format."""
        try:
            result = response.get("demographics", {}).get("response", {})
            if not result:
                return {"success": False, "message": "No demographics data found"}
                
            charts = result.get("charts", {})
            
            return {
                "success": True,
                "region_id": result.get("region", {}).get("id", ""),
                "region_name": result.get("region", {}).get("name", ""),
                "region_type": result.get("region", {}).get("type", ""),
                "demographics": {
                    "median_home_value": charts.get("home_values", {}).get("median_home_value", ""),
                    "median_income": charts.get("income", {}).get("median_income", ""),
                    "age_distribution": charts.get("ages", {}),
                    "education_level": charts.get("education", {}),
                    "marital_status": charts.get("marital_status", {})
                }
            }
        except Exception as e:
            logger.error(f"Error transforming demographics: {e}")
            return {"success": False, "message": f"Error transforming data: {str(e)}"}
    
    def _transform_region_children(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Zillow region children data to standardized format."""
        try:
            result = response.get("regionchildren", {}).get("response", {})
            if not result:
                return {"success": False, "message": "No region children found"}
                
            region = result.get("region", {})
            children = result.get("list", {}).get("region", [])
            
            if not isinstance(children, list):
                children = [children]
                
            transformed = {
                "success": True,
                "region": {
                    "id": region.get("id", ""),
                    "name": region.get("name", ""),
                    "type": region.get("type", ""),
                    "latitude": region.get("latitude", ""),
                    "longitude": region.get("longitude", "")
                },
                "children": []
            }
            
            for child in children:
                transformed["children"].append({
                    "id": child.get("id", ""),
                    "name": child.get("name", ""),
                    "type": child.get("type", ""),
                    "latitude": child.get("latitude", ""),
                    "longitude": child.get("longitude", "")
                })
                
            return transformed
        except Exception as e:
            logger.error(f"Error transforming region children: {e}")
            return {"success": False, "message": f"Error transforming data: {str(e)}"}
    
    def _extract_property_details(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract common property details from Zillow API responses."""
        return {
            "zpid": property_data.get("zpid", ""),
            "address": {
                "street": property_data.get("address", {}).get("street", ""),
                "city": property_data.get("address", {}).get("city", ""),
                "state": property_data.get("address", {}).get("state", ""),
                "zipcode": property_data.get("address", {}).get("zipcode", "")
            },
            "zestimate": property_data.get("zestimate", {}).get("amount", {}).get("value", ""),
            "details": {
                "bedrooms": property_data.get("bedrooms", ""),
                "bathrooms": property_data.get("bathrooms", ""),
                "year_built": property_data.get("yearBuilt", ""),
                "lot_size": property_data.get("lotSizeSqFt", ""),
                "finished_size": property_data.get("finishedSqFt", ""),
                "last_sold_date": property_data.get("lastSoldDate", ""),
                "last_sold_price": property_data.get("lastSoldPrice", {}).get("value", "")
            },
            "links": {
                "home_details": property_data.get("links", {}).get("homedetails", ""),
                "maps": property_data.get("links", {}).get("mapthishome", "")
            }
        }
    
    # Utility methods for property ID mapping and image handling
    
    async def map_zillow_to_internal_id(self, zpid: str) -> Optional[str]:
        """
        Map a Zillow property ID to an internal property ID.
        
        Args:
            zpid: Zillow property ID
            
        Returns:
            Internal property ID if found, None otherwise
        """
        try:
            from ..db.session import get_db
            from ..models.property_mapping import PropertyMapping
            
            # Get database session
            db = next(get_db())
            
            # Query for the mapping
            property_mapping = db.query(PropertyMapping).filter(PropertyMapping.zillow_property_id == zpid).first()
            
            if property_mapping:
                return property_mapping.internal_property_id
            
            # If no mapping found, return a placeholder (in production, you might want to return None)
            return f"internal-{zpid}"  # Placeholder implementation
        except Exception as e:
            logger.error(f"Error mapping Zillow ID to internal ID: {e}")
            return f"internal-{zpid}"  # Fallback to placeholder
    
    async def map_internal_to_zillow_id(self, internal_id: str) -> Optional[str]:
        """
        Map an internal property ID to a Zillow property ID.
        
        Args:
            internal_id: Internal property ID
            
        Returns:
            Zillow property ID if found, None otherwise
        """
        try:
            from ..db.session import get_db
            from ..models.property_mapping import PropertyMapping
            
            # Get database session
            db = next(get_db())
            
            # Query for the mapping
            property_mapping = db.query(PropertyMapping).filter(PropertyMapping.internal_property_id == internal_id).first()
            
            if property_mapping:
                return property_mapping.zillow_property_id
            
            # If no mapping found, try to extract from the internal ID if it follows our placeholder pattern
            if internal_id.startswith("internal-"):
                return internal_id[9:]
            
            return None
        except Exception as e:
            logger.error(f"Error mapping internal ID to Zillow ID: {e}")
            
            # Fallback to placeholder extraction
            if internal_id.startswith("internal-"):
                return internal_id[9:]
            return None
    
    async def store_zillow_image_locally(self, image_url: str) -> str:
        """
        Download and store a Zillow image locally.
        
        Args:
            image_url: URL of the image on Zillow
            
        Returns:
            Local path to the stored image
        """
        try:
            import uuid
            from pathlib import Path
            import os
            
            # Generate a unique filename
            filename = f"{uuid.uuid4()}.jpg"
            
            # Define the storage directory (ensure it exists)
            storage_dir = Path(settings.ZILLOW_IMAGE_STORAGE_PATH)
            os.makedirs(storage_dir, exist_ok=True)
            
            # Full path to the image
            image_path = storage_dir / filename
            
            # Download and save the image
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)
                response.raise_for_status()
                
                with open(image_path, "wb") as f:
                    f.write(response.content)
            
            # In a real application, you might return a URL instead of a file path
            return str(image_path)
        
        except Exception as e:
            logger.error(f"Error storing image locally: {e}")
            # Return the original URL as a fallback
            return image_url
    
    async def store_zillow_images_locally(self, image_urls: List[str]) -> List[Dict[str, str]]:
        """
        Download and store multiple Zillow images locally.
        
        Args:
            image_urls: List of URLs of images on Zillow
            
        Returns:
            List of dictionaries with original URLs and local paths
        """
        results = []
        for url in image_urls:
            local_path = await self.store_zillow_image_locally(url)
            results.append({
                "original_url": url,
                "local_path": local_path
            })
        return results
        
    async def save_property_images(self, property_id: str, image_urls: List[str]) -> List[Dict[str, Any]]:
        """
        Download Zillow images and save them to the database.
        
        Args:
            property_id: Internal property ID
            image_urls: List of Zillow image URLs
            
        Returns:
            List of saved image records
        """
        try:
            import uuid
            from ..db.session import get_db
            from ..models.property_image import PropertyImage
            
            # Get database session
            db = next(get_db())
            
            # Download and store images
            image_results = await self.store_zillow_images_locally(image_urls)
            
            # Save to database
            saved_images = []
            for image in image_results:
                # Create image record
                image_record = PropertyImage(
                    id=str(uuid.uuid4()),
                    property_id=property_id,
                    zillow_url=image["original_url"],
                    local_path=image["local_path"]
                )
                
                db.add(image_record)
                saved_images.append({
                    "id": image_record.id,
                    "property_id": image_record.property_id,
                    "zillow_url": image_record.zillow_url,
                    "local_path": image_record.local_path
                })
            
            # Commit changes
            db.commit()
            
            return saved_images
        except Exception as e:
            logger.error(f"Error saving property images: {e}")
            return []
            
    async def get_property_with_internal_id(self, internal_id: str) -> Dict[str, Any]:
        """
        Get property details using an internal property ID.
        
        Args:
            internal_id: Internal property ID
            
        Returns:
            Property details with both internal and Zillow IDs
        """
        # Map the internal ID to a Zillow ID
        zpid = await self.map_internal_to_zillow_id(internal_id)
        if not zpid:
            return {"success": False, "message": f"No Zillow ID found for internal ID: {internal_id}"}
        
        # Get the property details from Zillow
        zillow_details = await self.get_updated_property_details(zpid)
        if not zillow_details.get("success", False):
            return zillow_details
        
        # Add the internal ID to the response
        zillow_details["internal_id"] = internal_id
        
        return zillow_details