"""
Tests for the Zillow API endpoints.
"""
import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.core.dependencies import get_current_user

# Mock authenticated user for testing
async def mock_get_current_user():
    return {"id": "test-user-id", "email": "test@example.com", "is_active": True}

# Override the dependency
app.dependency_overrides[get_current_user] = mock_get_current_user

client = TestClient(app)

# Sample API responses for testing
SAMPLE_SEARCH_RESULT = {
    "success": True,
    "properties": [
        {
            "zpid": "12345678",
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zipcode": "90210"
            }
        }
    ]
}

SAMPLE_ZESTIMATE_RESULT = {
    "success": True,
    "zpid": "12345678",
    "zestimate": {
        "amount": "500000",
        "currency": "USD",
        "valuation_range": {
            "low": "450000",
            "high": "550000"
        }
    }
}

SAMPLE_COMPS_RESULT = {
    "success": True,
    "principal": {
        "zpid": "12345678",
        "address": "123 Main St",
        "zestimate": "500000"
    },
    "comparables": [
        {
            "zpid": "87654321",
            "address": "456 Oak St",
            "zestimate": "510000",
            "similarity_score": "0.95"
        }
    ]
}

@pytest.mark.asyncio
async def test_zillow_search_property():
    """Test the zillow_search_property endpoint."""
    with patch('app.services.zillow_api.ZillowAPIService.get_search_results', 
               new_callable=AsyncMock) as mock_search:
        # Configure the mock
        mock_search.return_value = SAMPLE_SEARCH_RESULT
        
        # Make the request
        response = client.get("/api/properties/zillow/search?address=123%20Main%20St&citystatezip=Anytown,%20CA%2090210")
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["properties"]) == 1
        assert data["properties"][0]["zpid"] == "12345678"
        
        # Verify the mock was called with the correct parameters
        mock_search.assert_called_once_with("123 Main St", "Anytown, CA 90210")

@pytest.mark.asyncio
async def test_zillow_get_zestimate():
    """Test the zillow_get_zestimate endpoint."""
    with patch('app.services.zillow_api.ZillowAPIService.get_zestimate', 
               new_callable=AsyncMock) as mock_zestimate:
        # Configure the mock
        mock_zestimate.return_value = SAMPLE_ZESTIMATE_RESULT
        
        # Make the request
        response = client.get("/api/properties/zillow/zestimate/12345678")
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["zpid"] == "12345678"
        assert data["zestimate"]["amount"] == "500000"
        
        # Verify the mock was called with the correct parameters
        mock_zestimate.assert_called_once_with("12345678")

@pytest.mark.asyncio
async def test_zillow_get_comps():
    """Test the zillow_get_comps endpoint."""
    with patch('app.services.zillow_api.ZillowAPIService.get_comps', 
               new_callable=AsyncMock) as mock_comps:
        # Configure the mock
        mock_comps.return_value = SAMPLE_COMPS_RESULT
        
        # Make the request
        response = client.get("/api/properties/zillow/comps/12345678?count=3")
        
        # Verify the response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["principal"]["zpid"] == "12345678"
        assert len(data["comparables"]) == 1
        
        # Verify the mock was called with the correct parameters
        mock_comps.assert_called_once_with("12345678", 3)

@pytest.mark.asyncio
async def test_zillow_error_handling():
    """Test error handling in Zillow API endpoints."""
    with patch('app.services.zillow_api.ZillowAPIService.get_search_results', 
               new_callable=AsyncMock) as mock_search:
        # Configure the mock to return an error
        mock_search.return_value = {"success": False, "message": "API error"}
        
        # Make the request
        response = client.get("/api/properties/zillow/search?address=123%20Main%20St&citystatezip=Anytown,%20CA%2090210")
        
        # Verify the response
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Property not found" in data["detail"]