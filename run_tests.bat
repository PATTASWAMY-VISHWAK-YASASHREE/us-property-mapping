@echo off
setlocal enabledelayedexpansion

:: Run tests for the Wealth Map Platform
echo Wealth Map Platform Test Runner

:: Set colors for better readability
set GREEN=[92m
set YELLOW=[93m
set RED=[91m
set NC=[0m

:: Check if a specific test was requested
if "%1"=="" (
    echo %YELLOW%Running specific backend tests (Zillow API and Email Service)...%NC%
    cd backend
    echo %GREEN%Running Zillow API tests...%NC%
    python -m pytest tests/test_zillow_api.py -v
    echo %GREEN%Running Email Service tests...%NC%
    python -m pytest tests/services/test_email_service.py -v
    cd ..
) else if "%1"=="all" (
    echo %YELLOW%Running all backend and frontend tests...%NC%
    
    echo %GREEN%Running backend tests...%NC%
    cd backend
    python -m pytest
    cd ..
    
    echo %GREEN%Running frontend tests...%NC%
    cd frontend
    call npm run test
    cd ..
) else if "%1"=="backend" (
    echo %YELLOW%Running all backend tests...%NC%
    cd backend
    python -m pytest
    cd ..
) else if "%1"=="frontend" (
    echo %YELLOW%Running frontend unit tests...%NC%
    cd frontend
    call npm run test
    cd ..
) else if "%1"=="e2e" (
    echo %YELLOW%Running frontend end-to-end tests...%NC%
    cd frontend
    call npm run test:e2e
    cd ..
) else if "%1"=="e2e:open" (
    echo %YELLOW%Opening Cypress for interactive end-to-end testing...%NC%
    cd frontend
    call npm run test:e2e:open
    cd ..
) else if "%1"=="coverage:frontend" (
    echo %YELLOW%Running frontend tests with coverage...%NC%
    cd frontend
    call npm run test:coverage
    cd ..
) else if "%1"=="coverage:backend" (
    echo %YELLOW%Running backend tests with coverage...%NC%
    cd backend
    python -m pytest --cov=app --cov-report=html
    echo %GREEN%Coverage report generated in backend/htmlcov/index.html%NC%
    cd ..
) else if "%1"=="lint" (
    echo %YELLOW%Running frontend linting...%NC%
    cd frontend
    call npm run lint
    cd ..
) else if "%1"=="unit" (
    echo %YELLOW%Running backend unit tests...%NC%
    cd backend
    python -m pytest -m unit
    cd ..
) else if "%1"=="api" (
    echo %YELLOW%Running backend API tests...%NC%
    cd backend
    python -m pytest -m api
    cd ..
) else if "%1"=="auth" (
    echo %YELLOW%Running authentication tests...%NC%
    cd backend
    python -m pytest -m auth
    cd ..
) else if "%1"=="property" (
    echo %YELLOW%Running backend property tests...%NC%
    cd backend
    python -m pytest -m property
    cd ..
) else if "%1"=="perf" (
    echo %YELLOW%Running performance tests...%NC%
    cd backend
    python -m pytest tests/performance/locustfile.py -v
    cd ..
) else (
    echo %YELLOW%Running tests matching pattern: %1%NC%
    cd backend
    python -m pytest %1 -v
    cd ..
)

echo %GREEN%Tests completed.%NC%
echo.
echo Usage:
echo   run_tests.bat                - Run specific backend tests (Zillow API and Email Service)
echo   run_tests.bat all            - Run all backend and frontend tests
echo   run_tests.bat backend        - Run all backend tests
echo   run_tests.bat frontend       - Run frontend unit tests
echo   run_tests.bat e2e            - Run frontend end-to-end tests
echo   run_tests.bat e2e:open       - Open Cypress for interactive end-to-end testing
echo   run_tests.bat coverage:frontend - Run frontend tests with coverage
echo   run_tests.bat coverage:backend  - Run backend tests with coverage
echo   run_tests.bat lint           - Run frontend linting
echo   run_tests.bat unit           - Run backend unit tests
echo   run_tests.bat api            - Run backend API tests
echo   run_tests.bat auth           - Run authentication tests
echo   run_tests.bat property       - Run backend property tests
echo   run_tests.bat perf           - Run performance tests
echo   run_tests.bat [pattern]      - Run backend tests matching pattern (e.g., tests/api/test_auth.py)