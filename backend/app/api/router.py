from fastapi import APIRouter

from app.api.endpoints import auth, users, properties, owners, search, reports, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["User Management"])
api_router.include_router(properties.router, prefix="/properties", tags=["Properties"])
api_router.include_router(owners.router, prefix="/owners", tags=["Owners"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])