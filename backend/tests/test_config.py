import os
import pytest
import json
from app.core.config import Settings

def test_cors_origins_empty():
    """Test CORS origins with empty string."""
    os.environ["BACKEND_CORS_ORIGINS"] = ""
    settings = Settings()
    assert settings.BACKEND_CORS_ORIGINS == []

def test_cors_origins_comma_separated():
    """Test CORS origins with comma-separated string."""
    os.environ["BACKEND_CORS_ORIGINS"] = "http://localhost:3000,http://localhost:8000"
    settings = Settings()
    assert settings.BACKEND_CORS_ORIGINS == ["http://localhost:3000", "http://localhost:8000"]

def test_cors_origins_json_string():
    """Test CORS origins with JSON string."""
    os.environ["BACKEND_CORS_ORIGINS"] = json.dumps(["http://localhost:3000", "http://localhost:8000"])
    settings = Settings()
    assert settings.BACKEND_CORS_ORIGINS == ["http://localhost:3000", "http://localhost:8000"]

def test_cors_origins_list():
    """Test CORS origins with list."""
    # This test simulates what happens when the validator receives a list directly
    settings = Settings()
    # Call the validator directly with a list
    result = settings.assemble_cors_origins(["http://localhost:3000", "http://localhost:8000"])
    assert result == ["http://localhost:3000", "http://localhost:8000"]

def test_cors_origins_invalid_type():
    """Test CORS origins with invalid type."""
    settings = Settings()
    # Call the validator directly with an invalid type
    result = settings.assemble_cors_origins(123)
    assert result == []