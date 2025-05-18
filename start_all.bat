@echo off
setlocal enabledelayedexpansion

:: Wealth Map Platform Ignition Key
:: This script starts all components of the Wealth Map Platform: backend, frontend, and database

:: Text color
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
where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :print_error "Docker is not installed. Please install Docker first."
    echo Visit https://docs.docker.com/get-docker/ for installation instructions.
    goto :docker_not_available
)

where docker-compose >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :print_error "Docker Compose is not installed. Please install Docker Compose first."
    echo Visit https://docs.docker.com/compose/install/ for installation instructions.
    goto :docker_not_available
)

echo %GREEN%✓%NC% Docker and Docker Compose are installed.
set DOCKER_AVAILABLE=1
goto :eof

:docker_not_available
set DOCKER_AVAILABLE=0
goto :eof

:: Check for required environment files
:check_env_files
if not exist .\backend\.env (
    call :print_warning "Backend environment file not found."
    set ENV_FILES_EXIST=0
) else (
    set ENV_FILES_EXIST=1
)

if not exist .\frontend\.env (
    call :print_warning "Frontend environment file not found."
    set ENV_FILES_EXIST=0
)

if %ENV_FILES_EXIST% EQU 0 (
    echo.
    echo %YELLOW%Would you like to run setup.bat to create the environment files? [Y/n]%NC%
    set /p run_setup=
    if not defined run_setup set run_setup=Y
    
    if /i "%run_setup%"=="Y" (
        call setup.bat
        exit /b 0
    ) else (
        call :print_warning "Continuing without proper environment files. Services may not work correctly."
    )
)
goto :eof

:: Start services using Docker Compose
:start_services_docker
call :print_section "Starting Services (Docker)"

echo Building and starting Docker containers...
docker-compose up -d
if %ERRORLEVEL% neq 0 (
    call :print_error "Failed to start Docker containers."
    pause
    exit /b 1
)

:: Wait for services to be ready
echo.
echo %YELLOW%Waiting for services to be ready...%NC%
timeout /t 5 /nobreak > nul

echo.
echo %GREEN%All services are now running!%NC%
echo.
echo %GREEN%Access your application at:%NC%
echo   - Frontend: http://localhost:8080
echo   - Backend API: http://localhost:8000
echo   - API Documentation: http://localhost:8000/docs
echo   - Database Admin (PgAdmin): http://localhost:5050
echo     - Email: admin@wealthmap.com
echo     - Password: admin

echo.
echo %YELLOW%To stop all services, press any key or run: docker-compose down%NC%
echo.

:: Keep the window open
pause > nul

:: Stop all services when the user presses a key
echo.
echo %GREEN%Stopping all services...%NC%
docker-compose down

echo.
echo %GREEN%All services have been stopped.%NC%
timeout /t 2 /nobreak > nul
goto :eof

:: Start services for local development (without Docker)
:start_services_local
call :print_section "Starting Services (Local Development)"

:: Check if PostgreSQL is installed
where psql >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :print_warning "PostgreSQL command line tools not found. Make sure PostgreSQL is installed and running."
) else (
    echo %GREEN%✓%NC% PostgreSQL is installed.
)

:: Remind user about PostgreSQL configuration
echo Please ensure PostgreSQL is running locally with the following configuration:
echo   - Database: wealth_map
echo   - Username: postgres
echo   - Password: vishwak
echo   - Port: 5432

:: Check if Python virtual environment exists
if not exist .\backend\venv (
    call :print_warning "Python virtual environment not found. Creating one..."
    cd backend
    python -m venv venv
    cd ..
)

:: Check if node_modules exists
if not exist .\frontend\node_modules (
    call :print_warning "Frontend dependencies not found. Installing..."
    cd frontend
    call npm install
    cd ..
)

:: Start backend in background
echo Starting backend server...
cd backend
call venv\Scripts\activate.bat
if not exist logs mkdir logs
start /B cmd /c "title Wealth Map Backend && color 0A && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > logs\backend.log 2>&1"
cd ..
echo %GREEN%✓%NC% Backend server started.

:: Start frontend in background
echo Starting frontend server...
cd frontend
start /B cmd /c "title Wealth Map Frontend && color 0B && npm run dev > ..\backend\logs\frontend.log 2>&1"
cd ..
echo %GREEN%✓%NC% Frontend server started.

echo.
echo %GREEN%Services are now running:%NC%
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:5173 or http://localhost:5174
echo   - API Documentation: http://localhost:8000/docs

echo.
echo %YELLOW%To stop the services, close the command prompt windows or use Task Manager%NC%
echo.
echo Press any key to exit this window (services will continue running)...
pause > nul
goto :eof

:: Main execution
:main
call :print_section "Wealth Map Platform Ignition Key"

:: Check Docker installation
call :check_docker

:: Check environment files
call :check_env_files

:: Determine startup method
if %DOCKER_AVAILABLE% EQU 1 (
    echo.
    echo %YELLOW%Choose startup method:%NC%
    echo 1. Docker (recommended, starts database, backend, and frontend)
    echo 2. Local development (requires local PostgreSQL)
    echo.
    set /p startup_method=Enter your choice [1]: 
    if not defined startup_method set startup_method=1
    
    if "%startup_method%"=="1" (
        call :start_services_docker
    ) else if "%startup_method%"=="2" (
        call :start_services_local
    ) else (
        call :print_error "Invalid choice. Using Docker by default."
        call :start_services_docker
    )
) else (
    call :print_warning "Docker not available. Using local development mode."
    call :start_services_local
)

goto :eof

:: Start the script
call :main