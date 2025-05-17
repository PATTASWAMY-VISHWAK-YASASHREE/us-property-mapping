from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Import and include routers
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.properties import router as properties_router
from app.api.owners import router as owners_router
from app.api.search import router as search_router
from app.api.reports import router as reports_router
from app.api.admin import router as admin_router

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/users", tags=["User Management"])
app.include_router(properties_router, prefix="/api/properties", tags=["Properties"])
app.include_router(owners_router, prefix="/api/owners", tags=["Owners"])
app.include_router(search_router, prefix="/api/search", tags=["Search"])
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Wealth Map API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)