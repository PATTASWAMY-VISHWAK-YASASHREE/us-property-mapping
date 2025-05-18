@echo off
echo Running authentication tests...

:: Stop any running Docker containers
echo Stopping any running Docker containers...
docker-compose down 2>nul

:: Run the auth tests
cd backend
python -m pytest tests/api/test_auth_flows.py -v

echo.
echo If you see errors about missing modules, run:
echo pip install pytest pytest-cov fastapi sqlalchemy pydantic python-jose[cryptography] passlib python-multipart httpx
echo.

cd ..

echo Tests completed.