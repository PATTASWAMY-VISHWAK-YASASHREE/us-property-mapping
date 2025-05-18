import pytest
import os
from unittest.mock import patch, MagicMock
from app.services.zillow_api import ZillowAPIService

@pytest.fixture
def zillow_service():
    return ZillowAPIService()

def test_zillow_api_key_is_set(zillow_service):
    """Test that the Zillow API key is set correctly."""
    assert zillow_service.api_key == "39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75"
    assert zillow_service.headers["X-RapidAPI-Key"] == "39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75"
    assert zillow_service.headers["X-RapidAPI-Host"] == "zillow-working-api.p.rapidapi.com"

def test_zillow_api_base_url(zillow_service):
    """Test that the Zillow API base URL is set correctly."""
    assert zillow_service.BASE_URL == "https://zillow-working-api.p.rapidapi.com"