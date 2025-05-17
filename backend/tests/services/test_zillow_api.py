"""
Tests for the Zillow API service.
"""
import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from app.services.zillow_api import ZillowAPIService, ZillowAPIException, ZillowAPIRateLimitException

# Sample API responses for testing
SAMPLE_SEARCH_RESPONSE = {
    "searchresults": {
        "response": {
            "results": {
                "result": {
                    "zpid": "12345678",
                    "address": {
                        "street": "123 Main St",
                        "city": "Anytown",
                        "state": "CA",
                        "zipcode": "90210",
                        "latitude": "34.0522",
                        "longitude": "-118.2437"
                    },
                    "links": {
                        "homedetails": "https://www.zillow.com/homedetails/12345678",
                        "mapthishome": "https://www.zillow.com/homes/12345678_map/",
                        "comparables": "https://www.zillow.com/homes/comps/12345678_zpid/"
                    }
                }
            }
        }
    }
}

SAMPLE_ZESTIMATE_RESPONSE = {
    "zestimate": {
        "response": {
            "zpid": "12345678",
            "zestimate": {
                "amount": {"value": "500000", "currency": "USD"},
                "last_updated": "2023-01-01",
                "valueChange": {"value": "10000"},
                "valuationRange": {
                    "low": {"value": "450000"},
                    "high": {"value": "550000"}
                },
                "percentile": "70"
            }
        }
    }
}

@pytest.fixture
def zillow_service():
    """Create a ZillowAPIService instance for testing."""
    service = ZillowAPIService()
    # Override the API key for testing
    service.api_key = "test_api_key"
    return service

@pytest.mark.asyncio
async def test_get_search_results(zillow_service):
    """Test the get_search_results method."""
    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_SEARCH_RESPONSE
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # Call the method
        result = await zillow_service.get_search_results("123 Main St", "Anytown, CA 90210")
        
        # Verify the result
        assert result["success"] is True
        assert len(result["properties"]) == 1
        assert result["properties"][0]["zpid"] == "12345678"
        assert result["properties"][0]["address"]["street"] == "123 Main St"

@pytest.mark.asyncio
async def test_get_zestimate(zillow_service):
    """Test the get_zestimate method."""
    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_ZESTIMATE_RESPONSE
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # Call the method
        result = await zillow_service.get_zestimate("12345678")
        
        # Verify the result
        assert result["success"] is True
        assert result["zpid"] == "12345678"
        assert result["zestimate"]["amount"] == "500000"
        assert result["zestimate"]["valuation_range"]["low"] == "450000"
        assert result["zestimate"]["valuation_range"]["high"] == "550000"

@pytest.mark.asyncio
async def test_rate_limit_handling(zillow_service):
    """Test handling of rate limit errors."""
    with patch('httpx.AsyncClient.get') as mock_get, \
         patch('time.sleep') as mock_sleep:  # Mock sleep to avoid waiting in tests
        
        # Configure the mock to return a rate limit error
        mock_response = MagicMock()
        mock_response.status_code = 429  # Rate limit exceeded
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # Call the method and expect an exception
        with pytest.raises(ZillowAPIRateLimitException):
            await zillow_service._make_request("/GetSearchResults", {"address": "123 Main St"})
        
        # Verify that retry was attempted
        assert mock_get.call_count > 1
        assert mock_sleep.call_count > 0

@pytest.mark.asyncio
async def test_caching(zillow_service):
    """Test that responses are cached and reused."""
    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_SEARCH_RESPONSE
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # Call the method twice with the same parameters
        params = {"address": "123 Main St", "citystatezip": "Anytown, CA 90210"}
        await zillow_service._make_request("/GetSearchResults", params)
        await zillow_service._make_request("/GetSearchResults", params)
        
        # Verify that the API was only called once
        assert mock_get.call_count == 1

@pytest.mark.asyncio
async def test_cache_expiry(zillow_service):
    """Test that cache entries expire after the specified time."""
    # Add a test entry to the cache with an expired timestamp
    cache_key = "/GetSearchResults:test"
    zillow_service._cache[cache_key] = {
        "data": {"test": "data"},
        "expires": datetime.now() - timedelta(seconds=1)  # Already expired
    }
    
    # Verify that the expired entry is not returned
    result = zillow_service._get_from_cache(cache_key)
    assert result is None
    
    # Verify that the expired entry was removed from the cache
    assert cache_key not in zillow_service._cache

@pytest.mark.asyncio
async def test_store_zillow_image_locally(zillow_service, tmp_path):
    """Test storing a Zillow image locally."""
    # Mock the image URL and httpx response
    image_url = "https://photos.zillowstatic.com/fp/test-image.jpg"
    
    with patch('httpx.AsyncClient.get') as mock_get, \
         patch('builtins.open', mock_open()) as mock_file, \
         patch.object(zillow_service, 'settings') as mock_settings:
        
        # Configure the mocks
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake image data"
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # Set the image storage path to a temporary directory
        mock_settings.ZILLOW_IMAGE_STORAGE_PATH = str(tmp_path)
        
        # Call the method
        result = await zillow_service.store_zillow_image_locally(image_url)
        
        # Verify the result
        assert result.startswith(str(tmp_path))
        assert mock_get.called
        mock_file().write.assert_called_once_with(b"fake image data")

@pytest.mark.asyncio
async def test_store_zillow_images_locally(zillow_service):
    """Test storing multiple Zillow images locally."""
    # Mock the image URLs
    image_urls = [
        "https://photos.zillowstatic.com/fp/image1.jpg",
        "https://photos.zillowstatic.com/fp/image2.jpg"
    ]
    
    # Mock the store_zillow_image_locally method
    with patch.object(zillow_service, 'store_zillow_image_locally') as mock_store:
        mock_store.side_effect = ["/tmp/image1.jpg", "/tmp/image2.jpg"]
        
        # Call the method
        results = await zillow_service.store_zillow_images_locally(image_urls)
        
        # Verify the results
        assert len(results) == 2
        assert results[0]["original_url"] == image_urls[0]
        assert results[0]["local_path"] == "/tmp/image1.jpg"
        assert results[1]["original_url"] == image_urls[1]
        assert results[1]["local_path"] == "/tmp/image2.jpg"
        
        # Verify the mock was called correctly
        assert mock_store.call_count == 2
        mock_store.assert_any_call(image_urls[0])
        mock_store.assert_any_call(image_urls[1])

@pytest.mark.asyncio
async def test_save_property_images(zillow_service):
    """Test saving property images to the database."""
    # Mock data
    property_id = "test-property-id"
    image_urls = [
        "https://photos.zillowstatic.com/fp/image1.jpg",
        "https://photos.zillowstatic.com/fp/image2.jpg"
    ]
    
    # Mock dependencies
    with patch('app.services.zillow_api.get_db') as mock_get_db, \
         patch('app.services.zillow_api.PropertyImage') as mock_property_image, \
         patch('app.services.zillow_api.uuid.uuid4') as mock_uuid, \
         patch.object(zillow_service, 'store_zillow_images_locally') as mock_store:
        
        # Configure mocks
        mock_db = MagicMock()
        mock_get_db.return_value.__next__.return_value = mock_db
        mock_uuid.side_effect = ["image-id-1", "image-id-2"]
        
        # Mock the store_zillow_images_locally method
        mock_store.return_value = [
            {"original_url": image_urls[0], "local_path": "/tmp/image1.jpg"},
            {"original_url": image_urls[1], "local_path": "/tmp/image2.jpg"}
        ]
        
        # Call the method
        results = await zillow_service.save_property_images(property_id, image_urls)
        
        # Verify results
        assert len(results) == 2
        assert results[0]["property_id"] == property_id
        assert results[0]["zillow_url"] == image_urls[0]
        assert results[0]["local_path"] == "/tmp/image1.jpg"
        assert results[1]["property_id"] == property_id
        assert results[1]["zillow_url"] == image_urls[1]
        assert results[1]["local_path"] == "/tmp/image2.jpg"
        
        # Verify database operations
        assert mock_db.add.call_count == 2
        assert mock_db.commit.call_count == 1

@pytest.mark.asyncio
async def test_property_id_mapping(zillow_service):
    """Test mapping between Zillow and internal property IDs."""
    # Mock the database query for Zillow to internal mapping
    with patch('app.services.zillow_api.get_db') as mock_get_db, \
         patch('app.services.zillow_api.PropertyMapping') as mock_mapping:
        
        # Configure the mock for successful mapping
        mock_db = MagicMock()
        mock_get_db.return_value.__next__.return_value = mock_db
        mock_query = mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = MagicMock(internal_property_id="internal-12345678")
        
        # Test Zillow to internal mapping
        internal_id = await zillow_service.map_zillow_to_internal_id("12345678")
        assert internal_id == "internal-12345678"
        
        # Configure the mock for failed mapping
        mock_filter.first.return_value = None
        
        # Test Zillow to internal mapping with fallback
        internal_id = await zillow_service.map_zillow_to_internal_id("87654321")
        assert internal_id == "internal-87654321"
    
    # Mock the database query for internal to Zillow mapping
    with patch('app.services.zillow_api.get_db') as mock_get_db, \
         patch('app.services.zillow_api.PropertyMapping') as mock_mapping:
        
        # Configure the mock for successful mapping
        mock_db = MagicMock()
        mock_get_db.return_value.__next__.return_value = mock_db
        mock_query = mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = MagicMock(zillow_property_id="12345678")
        
        # Test internal to Zillow mapping
        zillow_id = await zillow_service.map_internal_to_zillow_id("internal-12345678")
        assert zillow_id == "12345678"
        
        # Configure the mock for failed mapping
        mock_filter.first.return_value = None
        
        # Test internal to Zillow mapping with fallback
        zillow_id = await zillow_service.map_internal_to_zillow_id("internal-87654321")
        assert zillow_id == "87654321"
        
        # Test with invalid internal ID
        zillow_id = await zillow_service.map_internal_to_zillow_id("invalid-id")
        assert zillow_id is None