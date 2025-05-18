from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
import secrets
import re
from typing import Dict, Callable, List, Optional
import uuid
from datetime import datetime, timedelta

from app.db.init_db import init_db, create_initial_admin
from app.db.run_migrations import run_migrations
from app.db.session import SessionLocal
from app.api.router import api_router
from app.core.config import settings
from app.models.token import TokenBlacklist

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security logger
security_logger = logging.getLogger("security")
security_handler = logging.FileHandler(settings.SECURITY_LOG_FILE)
security_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
security_logger.addHandler(security_handler)
security_logger.setLevel(logging.INFO)

# Create FastAPI application with optimized settings
app = FastAPI(
    title="Wealth Map API",
    description="API for the Wealth Map Platform",
    version="1.0.0",
    # Optimize OpenAPI docs loading
    openapi_url="/api/openapi.json" if settings.ENVIRONMENT != "production" else None,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Performance monitoring middleware
class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log slow requests (over 200ms)
        if process_time > 0.2:
            logger.warning(f"Slow request: {request.method} {request.url.path} - {process_time:.4f}s")
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        return response

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        for header_name, header_value in settings.SECURITY_HEADERS.items():
            response.headers[header_name] = header_value
            
        return response

# Rate limiting middleware
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit_map: Dict[str, str] = None):
        super().__init__(app)
        self.rate_limits = {}  # path_pattern -> (requests, period_seconds)
        self.client_requests = {}  # client_id -> {path_pattern -> [(timestamp, request_id)]}
        
        # Parse rate limits
        if rate_limit_map:
            for path_pattern, limit in rate_limit_map.items():
                requests, period = limit.split("/")
                period_seconds = self._parse_period(period)
                self.rate_limits[path_pattern] = (int(requests), period_seconds)
    
    def _parse_period(self, period: str) -> int:
        """Convert period string to seconds"""
        if period.endswith("second"):
            return 1
        elif period.endswith("minute"):
            return 60
        elif period.endswith("hour"):
            return 3600
        elif period.endswith("day"):
            return 86400
        return 60  # Default to 1 minute
    
    def _get_client_id(self, request: Request) -> str:
        """Get a unique identifier for the client"""
        # Use X-Forwarded-For if behind a proxy, otherwise use client.host
        client_ip = request.headers.get("X-Forwarded-For", request.client.host)
        # Include user agent to differentiate between different clients from same IP
        user_agent = request.headers.get("User-Agent", "")
        return f"{client_ip}:{user_agent}"
    
    def _get_matching_rate_limit(self, path: str) -> Optional[tuple]:
        """Find the matching rate limit for the path"""
        for pattern, limit in self.rate_limits.items():
            if re.match(pattern, path):
                return limit
        return None
    
    def _clean_old_requests(self, client_id: str, path_pattern: str, period: int):
        """Remove requests older than the rate limit period"""
        now = time.time()
        if client_id in self.client_requests and path_pattern in self.client_requests[client_id]:
            self.client_requests[client_id][path_pattern] = [
                req for req in self.client_requests[client_id][path_pattern]
                if now - req[0] < period
            ]
    
    async def dispatch(self, request: Request, call_next):
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
            
        path = request.url.path
        client_id = self._get_client_id(request)
        rate_limit = self._get_matching_rate_limit(path)
        
        # If no specific rate limit matches, use default
        if not rate_limit and "/api/" in path:
            requests, period = settings.RATE_LIMIT_DEFAULT.split("/")
            rate_limit = (int(requests), self._parse_period(period))
        
        # Apply rate limiting if a limit is defined
        if rate_limit:
            max_requests, period = rate_limit
            
            # Initialize client request tracking
            if client_id not in self.client_requests:
                self.client_requests[client_id] = {}
            if path not in self.client_requests[client_id]:
                self.client_requests[client_id][path] = []
            
            # Clean old requests
            self._clean_old_requests(client_id, path, period)
            
            # Check if rate limit exceeded
            if len(self.client_requests[client_id][path]) >= max_requests:
                security_logger.warning(f"Rate limit exceeded: {client_id} - {path}")
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests"}
                )
            
            # Record this request
            request_id = str(uuid.uuid4())
            self.client_requests[client_id][path].append((time.time(), request_id))
            
            # Add rate limit headers
            response = await call_next(request)
            remaining = max_requests - len(self.client_requests[client_id][path])
            response.headers["X-RateLimit-Limit"] = str(max_requests)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(int(time.time() + period))
            return response
        
        return await call_next(request)

# SQL Injection Protection Middleware
class SQLInjectionProtectionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Common SQL injection patterns
        self.sql_patterns = [
            r"(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE)(\s|$)",
            r"(\s|^)(UNION|JOIN|OR|AND)(\s|$).*?SELECT",
            r"--",
            r";.*?$",
            r"/\*.*?\*/",
            r"'.*?'.*?=.*?'",
            r"\".*?\".*?=.*?\""
        ]
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.sql_patterns]
    
    def _check_sql_injection(self, value: str) -> bool:
        """Check if a string contains SQL injection patterns"""
        if not value:
            return False
            
        for pattern in self.compiled_patterns:
            if pattern.search(value):
                return True
        return False
    
    async def dispatch(self, request: Request, call_next):
        # Check query parameters
        for param, value in request.query_params.items():
            if self._check_sql_injection(value):
                security_logger.warning(f"Potential SQL injection detected in query param: {param}={value}")
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid request"}
                )
        
        # For POST/PUT requests, check the body
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                body = await request.body()
                body_str = body.decode()
                if self._check_sql_injection(body_str):
                    security_logger.warning(f"Potential SQL injection detected in request body")
                    return JSONResponse(
                        status_code=400,
                        content={"detail": "Invalid request"}
                    )
            except:
                # If we can't decode the body, continue
                pass
        
        return await call_next(request)

# Add performance monitoring
app.add_middleware(PerformanceMiddleware)

# Add security headers
app.add_middleware(SecurityHeadersMiddleware)

# Add SQL injection protection
app.add_middleware(SQLInjectionProtectionMiddleware)

# Add rate limiting
rate_limit_map = {
    r"^/api/auth/login$": settings.RATE_LIMIT_LOGIN,
    r"^/api/auth/register$": "10/hour",
    r"^/api/auth/password/reset$": "5/hour"
}
app.add_middleware(RateLimitMiddleware, rate_limit_map=rate_limit_map)

# Add session middleware with secure settings
app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.SECRET_KEY,
    max_age=3600,  # 1 hour
    https_only=settings.HTTPS_ONLY,
    same_site="lax"
)

# Add GZip compression for responses
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Configure CORS with specific origins for production
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "User-Agent"],
        expose_headers=["X-Process-Time", "X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"],
        max_age=3600,  # Cache preflight requests for 1 hour
    )
else:
    # Development mode - allow all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API router
app.include_router(api_router, prefix="/api")

# Health check endpoint (no auth required)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Wealth Map API"}

# Global exception handler for better error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )

@app.on_event("startup")
async def startup_event():
    logger.info("Starting application...")
    try:
        # Run SQL migrations
        run_migrations()
        
        # Initialize database tables
        init_db()
        
        # Create initial admin user
        db = SessionLocal()
        try:
            create_initial_admin(db)
            
            # Clean up expired tokens
            now = datetime.utcnow()
            db.query(TokenBlacklist).filter(
                TokenBlacklist.expires_at < now
            ).delete()
            db.commit()
            
        finally:
            db.close()
            
        logger.info("Database initialization completed successfully.")
        
        # Log startup
        security_logger.info("Application started")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    security_logger.info("Application shutdown")
    # Close any resources that need proper cleanup

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.ENVIRONMENT != "production",
        workers=4,  # Adjust based on CPU cores
        ssl_keyfile="/path/to/key.pem" if settings.HTTPS_ONLY and settings.ENVIRONMENT == "production" else None,
        ssl_certfile="/path/to/cert.pem" if settings.HTTPS_ONLY and settings.ENVIRONMENT == "production" else None,
    )