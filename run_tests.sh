#!/bin/bash

# Set colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display usage information
show_usage() {
  echo "Usage:"
  echo "  ./run_tests.sh                - Run specific backend tests (Zillow API and Email Service)"
  echo "  ./run_tests.sh all            - Run all backend and frontend tests"
  echo "  ./run_tests.sh backend        - Run all backend tests"
  echo "  ./run_tests.sh frontend       - Run frontend unit tests"
  echo "  ./run_tests.sh e2e            - Run frontend end-to-end tests"
  echo "  ./run_tests.sh e2e:open       - Open Cypress for interactive end-to-end testing"
  echo "  ./run_tests.sh coverage:frontend - Run frontend tests with coverage"
  echo "  ./run_tests.sh coverage:backend  - Run backend tests with coverage"
  echo "  ./run_tests.sh lint           - Run frontend linting"
  echo "  ./run_tests.sh unit           - Run backend unit tests"
  echo "  ./run_tests.sh api            - Run backend API tests"
  echo "  ./run_tests.sh auth           - Run authentication tests"
  echo "  ./run_tests.sh property       - Run backend property tests"
  echo "  ./run_tests.sh perf           - Run performance tests"
  echo "  ./run_tests.sh [pattern]      - Run backend tests matching pattern (e.g., tests/api/test_auth.py)"
}

# Run tests based on the argument provided
if [ -z "$1" ]; then
  echo -e "${YELLOW}Running specific backend tests (Zillow API and Email Service)...${NC}"
  cd backend
  echo -e "${GREEN}Running Zillow API tests...${NC}"
  python -m pytest tests/test_zillow_api.py -v
  echo -e "${GREEN}Running Email Service tests...${NC}"
  python -m pytest tests/services/test_email_service.py -v
  cd ..
elif [ "$1" = "all" ]; then
  echo -e "${YELLOW}Running all backend and frontend tests...${NC}"
  
  echo -e "${GREEN}Running backend tests...${NC}"
  cd backend
  python -m pytest
  cd ..
  
  echo -e "${GREEN}Running frontend tests...${NC}"
  cd frontend
  npm run test
  cd ..
elif [ "$1" = "backend" ]; then
  echo -e "${YELLOW}Running all backend tests...${NC}"
  cd backend
  python -m pytest
  cd ..
elif [ "$1" = "frontend" ]; then
  echo -e "${YELLOW}Running frontend unit tests...${NC}"
  cd frontend
  npm run test
  cd ..
elif [ "$1" = "e2e" ]; then
  echo -e "${YELLOW}Running frontend end-to-end tests...${NC}"
  cd frontend
  npm run test:e2e
  cd ..
elif [ "$1" = "e2e:open" ]; then
  echo -e "${YELLOW}Opening Cypress for interactive end-to-end testing...${NC}"
  cd frontend
  npm run test:e2e:open
  cd ..
elif [ "$1" = "coverage:frontend" ]; then
  echo -e "${YELLOW}Running frontend tests with coverage...${NC}"
  cd frontend
  npm run test:coverage
  cd ..
elif [ "$1" = "coverage:backend" ]; then
  echo -e "${YELLOW}Running backend tests with coverage...${NC}"
  cd backend
  python -m pytest --cov=app --cov-report=html
  echo -e "${GREEN}Coverage report generated in backend/htmlcov/index.html${NC}"
  cd ..
elif [ "$1" = "lint" ]; then
  echo -e "${YELLOW}Running frontend linting...${NC}"
  cd frontend
  npm run lint
  cd ..
elif [ "$1" = "unit" ]; then
  echo -e "${YELLOW}Running backend unit tests...${NC}"
  cd backend
  python -m pytest -m unit
  cd ..
elif [ "$1" = "api" ]; then
  echo -e "${YELLOW}Running backend API tests...${NC}"
  cd backend
  python -m pytest -m api
  cd ..
elif [ "$1" = "auth" ]; then
  echo -e "${YELLOW}Running authentication tests...${NC}"
  cd backend
  python -m pytest -m auth
  cd ..
elif [ "$1" = "property" ]; then
  echo -e "${YELLOW}Running backend property tests...${NC}"
  cd backend
  python -m pytest -m property
  cd ..
elif [ "$1" = "perf" ]; then
  echo -e "${YELLOW}Running performance tests...${NC}"
  cd backend
  python -m pytest tests/performance/locustfile.py -v
  cd ..
else
  echo -e "${YELLOW}Running tests matching pattern: $1${NC}"
  cd backend
  python -m pytest $1 -v
  cd ..
fi

echo -e "${GREEN}Tests completed.${NC}"
echo
show_usage