@echo off
echo Fixing test environment...

:: Stop any running Docker containers
echo Stopping any running Docker containers...
docker-compose down 2>nul

:: Install required packages
echo Installing required packages...
pip install pytest pytest-cov fastapi sqlalchemy pydantic python-jose[cryptography] passlib python-multipart httpx

:: Run the auth tests
echo Running authentication tests...
cd backend
python -m pytest tests/api/test_auth_flows.py -v
cd ..

echo Tests completed.