@echo off
setlocal enabledelayedexpansion

:: Wealth Map Platform Setup Script for Windows
:: This script installs all requirements and starts all servers for the Wealth Map Platform

:: Text colors
set GREEN=[92m
set YELLOW=[93m
set RED=[91m
set NC=[0m

:: Function to print section headers
:print_section
echo.
echo %GREEN%==== %~1 ====%NC%
echo.
goto :eof

:: Function to print errors
:print_error
echo %RED%ERROR: %~1%NC%
goto :eof

:: Function to print warnings
:print_warning
echo %YELLOW%WARNING: %~1%NC%
goto :eof

:: Check if Docker and Docker Compose are installed
:check_docker
call :print_section "Checking Docker Installation"

where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :print_error "Docker is not installed. Please install Docker first."
    echo Visit https://docs.docker.com/get-docker/ for installation instructions.
    exit /b 1
)

where docker-compose >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :print_error "Docker Compose is not installed. Please install Docker Compose first."
    echo Visit https://docs.docker.com/compose/install/ for installation instructions.
    exit /b 1
)

echo %GREEN%✓%NC% Docker and Docker Compose are installed.
goto :eof

:: Check for required environment variables
:check_env_vars
call :print_section "Checking Environment Variables"

:: Create .env files if they don't exist
if not exist .\backend\.env (
    echo Creating backend/.env file with default values...
    (
        echo # Database
        echo DATABASE_URL=postgresql://postgres:vishwak@db:5432/wealth_map
        echo.
        echo # Security
        echo SECRET_KEY=dev_secret_key_for_local_development_only
        echo ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=60
        echo REFRESH_TOKEN_EXPIRE_DAYS=7
        echo MFA_ENABLED=true
        echo MFA_ISSUER=WealthMapAPI
        echo MFA_REQUIRED=false
        echo.
        echo # API Keys
        echo RAPIDAPI_KEY=your_rapidapi_key_here
        echo MAPBOX_API_KEY=your_mapbox_api_key_here
        echo.
        echo # Zillow API Settings
        echo ZILLOW_API_HOST=zillow-com1.p.rapidapi.com
        echo ZILLOW_CACHE_EXPIRY=3600
        echo ZILLOW_MAX_RETRIES=3
        echo ZILLOW_RETRY_DELAY=2
        echo ZILLOW_IMAGE_STORAGE_PATH=/tmp/property_images
        echo.
        echo # Environment
        echo ENVIRONMENT=development
        echo MOCK_EXTERNAL_APIS=true
        echo.
        echo # Logging
        echo LOG_LEVEL=DEBUG
        echo SECURITY_LOG_FILE=/app/logs/security.log
        echo.
        echo # HTTPS settings
        echo HTTPS_ONLY=false
        echo.
        echo # Frontend URL
        echo FRONTEND_URL=http://localhost:8080
        echo.
        echo # Rate limiting
        echo RATE_LIMIT_ENABLED=false
        echo RATE_LIMIT_DEFAULT=100/minute
        echo RATE_LIMIT_LOGIN=5/minute
        echo.
        echo # Email settings
        echo SMTP_SERVER=
        echo SMTP_PORT=587
        echo SMTP_USERNAME=
        echo SMTP_PASSWORD=
        echo SMTP_SENDER=noreply@wealthmap.com
        echo SMTP_TLS=true
    ) > .\backend\.env
    call :print_warning "Backend .env file created with default values. Please update with your actual API keys."
) else (
    echo %GREEN%✓%NC% Backend .env file exists.
)

if not exist .\frontend\.env (
    echo Creating frontend/.env file with default values...
    (
        echo VITE_API_URL=http://localhost:8000
        echo VITE_MAPBOX_TOKEN=your_mapbox_token_here
    ) > .\frontend\.env
    call :print_warning "Frontend .env file created with default values. Please update with your actual API keys."
) else (
    echo %GREEN%✓%NC% Frontend .env file exists.
)

:: Create logs directory for backend
if not exist .\backend\logs mkdir .\backend\logs
type nul > .\backend\logs\security.log
echo %GREEN%✓%NC% Created logs directory and security log file.
goto :eof

:: Install dependencies for local development (without Docker)
:install_dependencies_local
call :print_section "Installing Dependencies (Local Development)"

:: Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
call npm install
if %ERRORLEVEL% neq 0 (
    call :print_error "Failed to install frontend dependencies."
    exit /b 1
)
cd ..
echo %GREEN%✓%NC% Frontend dependencies installed.

:: Install backend dependencies
echo Installing backend dependencies...
cd backend

:: Check if Python virtual environment exists, create if not
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    call :print_error "Failed to install backend dependencies."
    exit /b 1
)

cd ..
echo %GREEN%✓%NC% Backend dependencies installed.
goto :eof

:: Start services for local development (without Docker)
:start_services_local
call :print_section "Starting Services (Local Development)"

:: Start PostgreSQL (assuming it's installed locally)
echo Please ensure PostgreSQL is running locally with the following configuration:
echo   - Database: wealth_map
echo   - Username: postgres
echo   - Password: vishwak
echo   - Port: 5432

:: Start backend in background
echo Starting backend server...
cd backend
call venv\Scripts\activate.bat
start /B cmd /c "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > logs\backend.log 2>&1"
cd ..
echo %GREEN%✓%NC% Backend server started.

:: Start frontend in background
echo Starting frontend server...
cd frontend
start /B cmd /c "npm run dev > ..\backend\logs\frontend.log 2>&1"
cd ..
echo %GREEN%✓%NC% Frontend server started.

echo.
echo %GREEN%Services are now running:%NC%
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:5173
echo   - API Documentation: http://localhost:8000/docs

echo.
echo %YELLOW%To stop the services, close the command prompt windows or use Task Manager%NC%
goto :eof

:: Start services using Docker Compose
:start_services_docker
call :print_section "Starting Services (Docker)"

echo Building and starting Docker containers...
docker-compose up -d
if %ERRORLEVEL% neq 0 (
    call :print_error "Failed to start Docker containers."
    exit /b 1
)

echo.
echo %GREEN%Services are now running:%NC%
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:8080
echo   - API Documentation: http://localhost:8000/docs
echo   - PgAdmin: http://localhost:5050
echo     - Email: admin@wealthmap.com
echo     - Password: admin

echo.
echo %YELLOW%To stop the services, run: docker-compose down%NC%
goto :eof

:: Main execution
:main
call :print_section "Wealth Map Platform Setup"

:: Check Docker installation
call :check_docker

:: Check and create environment files
call :check_env_vars

:: Ask user whether to use Docker or local development
echo.
set /p use_docker=Do you want to use Docker for development? (Recommended) [Y/n]: 
if not defined use_docker set use_docker=Y

if /i "%use_docker%"=="Y" (
    :: Docker-based setup
    call :start_services_docker
) else (
    :: Local development setup
    call :install_dependencies_local
    call :start_services_local
)

call :print_section "Setup Complete"
echo Please check the requirements.md file for more information about API keys and dependencies.
goto :eof

:: Start the script
call :main