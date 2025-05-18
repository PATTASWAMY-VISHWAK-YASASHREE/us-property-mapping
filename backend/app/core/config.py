import os
from pydantic import BaseSettings, validator
from typing import Optional, Dict, Any, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Wealth Map API"
    API_V1_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # Token settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))  # Reduced to 15 minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # MFA settings
    MFA_ENABLED: bool = os.getenv("MFA_ENABLED", "True").lower() == "true"
    MFA_ISSUER: str = os.getenv("MFA_ISSUER", "WealthMapAPI")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/wealth_map")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = os.getenv("BACKEND_CORS_ORIGINS", "").split(",")
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str) -> List[str]:
        if isinstance(v, str) and not v.strip():
            return []
        if isinstance(v, (list, str)):
            return [origin.strip() for origin in v.split(",") if origin]
        raise ValueError(v)
    
    # Security headers
    SECURITY_HEADERS: Dict[str, str] = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none';",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_DEFAULT: str = os.getenv("RATE_LIMIT_DEFAULT", "100/minute")
    RATE_LIMIT_LOGIN: str = os.getenv("RATE_LIMIT_LOGIN", "5/minute")
    
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
    
    # Encryption
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", SECRET_KEY)
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SECURITY_LOG_FILE: str = os.getenv("SECURITY_LOG_FILE", "/var/log/wealth_map_security.log")
    
    # HTTPS settings
    HTTPS_ONLY: bool = os.getenv("HTTPS_ONLY", "True").lower() == "true"
    
    class Config:
        case_sensitive = True

settings = Settings()