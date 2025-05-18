# Wealth Map Testing Guide

This document provides comprehensive instructions for running the various tests implemented in the Wealth Map platform.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Unit Testing](#unit-testing)
   - [Backend Unit Tests](#backend-unit-tests)
   - [Frontend Unit Tests](#frontend-unit-tests)
3. [Integration Testing](#integration-testing)
   - [API Integration Tests](#api-integration-tests)
   - [Authentication Flow Tests](#authentication-flow-tests)
4. [End-to-End Testing](#end-to-end-testing)
   - [Cypress E2E Tests](#cypress-e2e-tests)
   - [User Flow Tests](#user-flow-tests)
   - [Responsive Design Tests](#responsive-design-tests)
5. [Performance Testing](#performance-testing)
   - [Load Testing](#load-testing)
   - [Database Query Performance](#database-query-performance)
   - [API Response Time](#api-response-time)
6. [Code Coverage](#code-coverage)
   - [Backend Coverage](#backend-coverage)
   - [Frontend Coverage](#frontend-coverage)
7. [Continuous Integration](#continuous-integration)

## Prerequisites

Before running the tests, ensure you have the following installed:

- Node.js (v16+) and npm for frontend tests
- Python 3.8+ for backend tests
- Docker and Docker Compose for running the full application stack

## Running Tests

### Using the Test Runner Scripts

For convenience, we provide scripts to run various tests:

#### Linux/macOS:
```bash
# Run specific backend tests
./run_tests.sh

# Run all tests
./run_tests.sh all
```

#### Windows:
```batch
# Run specific backend tests
run_tests.bat

# Run all backend and frontend tests
run_tests.bat all

# Run only backend tests
run_tests.bat backend

# Run only frontend tests
run_tests.bat frontend

# Run end-to-end tests
run_tests.bat e2e

# Open Cypress for interactive testing
run_tests.bat e2e:open

# Run frontend tests with coverage
run_tests.bat coverage:frontend

# Run backend tests with coverage
run_tests.bat coverage:backend

# Run frontend linting
run_tests.bat lint

# Run specific test categories
run_tests.bat unit       # Backend unit tests
run_tests.bat api        # Backend API tests
run_tests.bat auth       # Authentication tests
run_tests.bat property   # Property tests
run_tests.bat perf       # Performance tests

# Run tests matching a specific pattern
run_tests.bat tests/api/test_auth.py
```

## Unit Testing

### Backend Unit Tests

The backend uses pytest for unit testing. To run the backend tests:

```bash
cd backend
pip install -r requirements.txt
pytest
```

To run specific test categories:

```bash
# Run only unit tests
pytest -m unit

# Run only API tests
pytest -m api

# Run only authentication tests
pytest -m auth

# Run tests with coverage report
pytest --cov=app --cov-report=html
```

### Frontend Unit Tests

The frontend uses Vitest for unit testing. To run the frontend tests:

```bash
cd frontend
npm install
npm test
```

To run tests in watch mode:

```bash
npm run test:watch
```

To generate a coverage report:

```bash
npm run test:coverage
```

## Integration Testing

### API Integration Tests

Integration tests verify that API endpoints work correctly with real database connections:

```bash
cd backend
pytest -m integration
```

### Authentication Flow Tests

Tests for complete authentication flows:

```bash
cd backend
pytest tests/api/test_auth_flows.py
```

## End-to-End Testing

### Cypress E2E Tests

The project uses Cypress for end-to-end testing. First, ensure the application is running:

```bash
# In one terminal
docker-compose up
```

Then, in another terminal:

```bash
cd frontend
npm run test:e2e
```

To open the Cypress UI for interactive testing:

```bash
npm run test:e2e:open
```

### User Flow Tests

To run specific user flow tests:

```bash
cd frontend
npx cypress run --spec "cypress/e2e/flows/report-generation.cy.js"
```

### Responsive Design Tests

To run responsive design tests across different device sizes:

```bash
cd frontend
npx cypress run --spec "cypress/e2e/ui/responsive.cy.js"
```

## Performance Testing

### Load Testing

The project uses Locust for load testing. To run load tests:

```bash
cd backend
locust -f tests/performance/locustfile.py
```

Then open http://localhost:8089 in your browser to configure and start the test.

To run headless load tests:

```bash
locust -f tests/performance/locustfile.py --headless -u 100 -r 10 --run-time 1m
```

### Database Query Performance

To specifically test database query performance:

```bash
locust -f tests/performance/locustfile.py --tags db_benchmark --headless -u 20 -r 5 --run-time 2m
```

### API Response Time

To measure API response times:

```bash
locust -f tests/performance/locustfile.py --tags api_response --headless -u 50 -r 10 --run-time 2m
```

## Code Coverage

### Backend Coverage

The backend tests are configured to generate coverage reports. To view the coverage:

```bash
cd backend
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in your browser
```

### Frontend Coverage

For frontend coverage:

```bash
cd frontend
npm run test:coverage
# Open coverage/index.html in your browser
```

## Continuous Integration

The project is configured to run tests automatically in CI/CD pipelines. The following tests are run:

1. Backend unit and integration tests
2. Frontend unit tests
3. Code linting and formatting checks
4. Code coverage checks (minimum 80% coverage required)

To run all CI checks locally:

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run lint
npm test
```

## Best Practices

1. **Write tests before code**: Follow Test-Driven Development (TDD) principles when possible.
2. **Keep tests independent**: Each test should be able to run independently of others.
3. **Use meaningful test names**: Test names should describe what is being tested.
4. **Mock external dependencies**: Use mocks for external APIs and services.
5. **Maintain test coverage**: Aim for at least 80% code coverage.
6. **Test edge cases**: Include tests for error conditions and edge cases.
7. **Run tests locally**: Always run tests locally before pushing code.