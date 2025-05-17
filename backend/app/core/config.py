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
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        case_sensitive = True

settings = Settings()