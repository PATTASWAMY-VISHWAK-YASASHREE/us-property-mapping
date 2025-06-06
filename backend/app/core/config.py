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
    MFA_REQUIRED: bool = os.getenv("MFA_REQUIRED", "True").lower() == "true"  # Require MFA for all users
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/wealth_map")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = os.getenv("BACKEND_CORS_ORIGINS", "")
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v) -> List[str]:
        """Process CORS origins from different input types.
        
        Handles:
        - Empty string or None: Returns empty list
        - String with comma-separated values: Splits and returns as list
        - JSON string containing a list: Parses and returns as list
        - List: Returns as is (after stripping)
        - Any other type: Returns empty list
        """
        if v is None:
            return []
            
        if isinstance(v, str):
            if not v.strip():
                return []
            try:
                # Try to parse as JSON
                import json
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [origin.strip() for origin in parsed if origin]
            except (json.JSONDecodeError, ValueError):
                # Not JSON, treat as comma-separated string
                return [origin.strip() for origin in v.split(",") if origin]
                
        if isinstance(v, list):
            return [str(origin).strip() for origin in v if origin]
            
        # For any other type, return empty list
        return []
    
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
    RAPIDAPI_KEY: str = "39ce75c22bmshef6d5494d5847e1p1579c2jsn0cb5a524de75"  # Hardcoded Zillow Rapid API key
    # MAPBOX_API_KEY: Optional[str] = os.getenv("MAPBOX_API_KEY")  # Mapbox API key not needed
    
    # Zillow API Settings
    ZILLOW_API_HOST: str = "zillow-working-api.p.rapidapi.com"
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
    
    # Frontend URL for links in emails
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Email settings
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: Optional[str] = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    SMTP_SENDER: str = os.getenv("SMTP_SENDER", "noreply@wealthmap.com")
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "True").lower() == "true"
    
    # Invitation settings
    INVITATION_EXPIRE_DAYS: int = int(os.getenv("INVITATION_EXPIRE_DAYS", "7"))
    
    # Map settings
    MAP_TILE_CACHE_EXPIRY: int = int(os.getenv("MAP_TILE_CACHE_EXPIRY", "86400"))  # 24 hours in seconds
    
    class Config:
        case_sensitive = True

settings = Settings()