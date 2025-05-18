from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.init_db import init_db, create_initial_admin
from app.db.run_migrations import run_migrations
from app.db.session import SessionLocal
from app.api.router import api_router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

# Add performance monitoring
app.add_middleware(PerformanceMiddleware)

# Add GZip compression for responses
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Configure CORS with specific origins for production
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
        finally:
            db.close()
            
        logger.info("Database initialization completed successfully.")
        
        # Warm up cache for common queries
        logger.info("Warming up cache...")
        # Add cache warming logic here if needed
        
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")
    # Close any resources that need proper cleanup

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.ENVIRONMENT != "production",
        workers=4  # Adjust based on CPU cores
    )