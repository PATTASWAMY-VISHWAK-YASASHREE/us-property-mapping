import os
from pydantic import BaseSettings
from typing import Optional, Dict, Any, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Wealth Map API"
    API_V1_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/wealth_map")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # API Keys
    RAPIDAPI_KEY: Optional[str] = os.getenv("RAPIDAPI_KEY")
    
    # Zillow API Settings
    ZILLOW_API_HOST: str = os.getenv("ZILLOW_API_HOST", "zillow-com1.p.rapidapi.com")
    ZILLOW_CACHE_EXPIRY: int = int(os.getenv("ZILLOW_CACHE_EXPIRY", "3600"))  # 1 hour in seconds
    ZILLOW_MAX_RETRIES: int = int(os.getenv("ZILLOW_MAX_RETRIES", "3"))
    ZILLOW_RETRY_DELAY: int = int(os.getenv("ZILLOW_RETRY_DELAY", "2"))  # seconds
    ZILLOW_IMAGE_STORAGE_PATH: str = os.getenv("ZILLOW_IMAGE_STORAGE_PATH", "/tmp/property_images")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        case_sensitive = True

settings = Settings()