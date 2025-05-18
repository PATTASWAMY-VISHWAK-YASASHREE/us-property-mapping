@echo off
setlocal enabledelayedexpansion

:: Run tests for the Wealth Map Platform
echo Wealth Map Platform Test Runner

:: Set environment variables for tests
set DATABASE_URL=postgresql://postgres:vishwak@localhost:5432/wealth_map

:: Check if a specific test was requested
if "%1"=="" (
    echo Running specific backend tests (Zillow API and Email Service)...
    cd backend
    echo Running database connection test...
    python -m pytest tests/test_db_connection.py -v
    echo Running Zillow API tests...
    python -m pytest tests/test_zillow_api.py -v
    echo Running Email Service tests...
    python -m pytest tests/services/test_email_service.py -v
    cd ..
) else if "%1"=="all" (
    echo Running all backend and frontend tests...
    
    echo Running backend tests...
    cd backend
    python -m pytest
    cd ..
    
    echo Running frontend tests...
    cd frontend
    call npm run test
    cd ..
) else if "%1"=="backend" (
    echo Running all backend tests...
    cd backend
    python -m pytest
    cd ..
) else if "%1"=="frontend" (
    echo Running frontend unit tests...
    cd frontend
    call npm run test
    cd ..
) else if "%1"=="e2e" (
    echo Running frontend end-to-end tests...
    cd frontend
    call npm run test:e2e
    cd ..
) else if "%1"=="e2e:open" (
    echo Opening Cypress for interactive end-to-end testing...
    cd frontend
    call npm run test:e2e:open
    cd ..
) else if "%1"=="coverage:frontend" (
    echo Running frontend tests with coverage...
    cd frontend
    call npm run test:coverage
    cd ..
) else if "%1"=="coverage:backend" (
    echo Running backend tests with coverage...
    cd backend
    python -m pytest --cov=app --cov-report=html
    echo Coverage report generated in backend/htmlcov/index.html
    cd ..
) else if "%1"=="lint" (
    echo Running frontend linting...
    cd frontend
    call npm run lint
    cd ..
) else if "%1"=="unit" (
    echo Running backend unit tests...
    cd backend
    python -m pytest -m unit
    cd ..
) else if "%1"=="api" (
    echo Running backend API tests...
    cd backend
    python -m pytest -m api
    cd ..
) else if "%1"=="auth" (
    echo Running authentication tests...
    cd backend
    python -m pytest -m auth
    cd ..
) else if "%1"=="property" (
    echo Running backend property tests...
    cd backend
    python -m pytest -m property
    cd ..
) else if "%1"=="db" (
    echo Running database connection test...
    cd backend
    python -m pytest tests/test_db_connection.py -v
    cd ..
) else if "%1"=="perf" (
    echo Running performance tests...
    cd backend
    python -m pytest tests/performance/locustfile.py -v
    cd ..
) else (
    echo Running tests matching pattern: %1
    cd backend
    python -m pytest %1 -v
    cd ..
)