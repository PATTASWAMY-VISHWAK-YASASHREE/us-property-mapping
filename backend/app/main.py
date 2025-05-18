from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.db.init_db import init_db, create_initial_admin
from app.db.run_migrations import run_migrations
from app.db.session import SessionLocal
from app.api.router import api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Wealth Map API",
    description="API for the Wealth Map Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the Wealth Map API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
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
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)