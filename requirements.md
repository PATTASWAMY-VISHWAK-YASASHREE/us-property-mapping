# Wealth Map Platform Requirements

This document outlines all the requirements, dependencies, API keys, and setup instructions for the Wealth Map Platform.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [API Keys](#api-keys)
3. [Backend Dependencies](#backend-dependencies)
4. [Frontend Dependencies](#frontend-dependencies)
5. [Environment Variables](#environment-variables)
6. [Database Setup](#database-setup)
7. [Development Workflow](#development-workflow)
8. [Deployment](#deployment)

## System Requirements

### For Docker-based Development (Recommended)

- Docker Engine (20.10.x or newer)
- Docker Compose (2.x or newer)
- At least 4GB of RAM allocated to Docker
- 10GB of free disk space

### For Local Development

- Node.js (16.x or newer)
- npm (8.x or newer)
- Python (3.8 or newer)
- pip (21.x or newer)
- PostgreSQL (12.x or newer) with PostGIS extension
- Git

## API Keys

The following API keys are required for full functionality:

### RapidAPI Key (for Zillow API)

The platform uses Zillow's API through RapidAPI to provide property data, valuations, and market insights.

1. Register for a [RapidAPI account](https://rapidapi.com/auth/sign-up)
2. Subscribe to the [Zillow API on RapidAPI](https://rapidapi.com/apimaker/api/zillow-com1/)
3. Retrieve your API key and configure it in the environment variables

**Environment Variable:** `RAPIDAPI_KEY`

### Mapbox API Key

Mapbox is used for interactive maps and geospatial features.

1. Create a [Mapbox account](https://account.mapbox.com/auth/signup/)
2. Navigate to your account dashboard and create an access token
3. Configure the token in the environment variables

**Environment Variables:**
- Backend: `MAPBOX_API_KEY`
- Frontend: `VITE_MAPBOX_TOKEN`

## Backend Dependencies

The backend is built with FastAPI and uses the following key dependencies:

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running the FastAPI application
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation and settings management
- **Python-jose**: JWT token handling
- **Passlib**: Password hashing
- **Alembic**: Database migrations
- **Psycopg2**: PostgreSQL adapter
- **Requests**: HTTP library
- **PyOTP**: One-time password generation for MFA
- **QRCode**: QR code generation for MFA setup
- **Pillow**: Image processing
- **Cryptography**: Cryptographic recipes and primitives
- **Python-dotenv**: Environment variable management

For a complete list with version specifications, see [backend/requirements.txt](./backend/requirements.txt).

## Frontend Dependencies

The frontend is built with Vue.js 3 and uses the following key dependencies:

- **Vue.js 3**: Progressive JavaScript framework
- **Vue Router**: Official router for Vue.js
- **Pinia**: State management for Vue
- **Axios**: HTTP client
- **Leaflet**: Interactive maps
- **Mapbox GL**: Advanced mapping features
- **Chart.js**: Data visualization
- **Tailwind CSS**: Utility-first CSS framework
- **Headless UI**: Unstyled, accessible UI components
- **Heroicons**: SVG icons

For development:
- **Vite**: Next-generation frontend tooling
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **Vitest**: Unit testing
- **Cypress**: End-to-end testing

For a complete list with version specifications, see [frontend/package.json](./frontend/package.json).

## Environment Variables

### Backend Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/wealth_map

# Security
SECRET_KEY=your_secure_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
MFA_ENABLED=true
MFA_ISSUER=WealthMapAPI
MFA_REQUIRED=false

# API Keys
RAPIDAPI_KEY=your_rapidapi_key_here
MAPBOX_API_KEY=your_mapbox_api_key_here

# Zillow API Settings
ZILLOW_API_HOST=zillow-com1.p.rapidapi.com
ZILLOW_CACHE_EXPIRY=3600
ZILLOW_MAX_RETRIES=3
ZILLOW_RETRY_DELAY=2
ZILLOW_IMAGE_STORAGE_PATH=/tmp/property_images

# Environment
ENVIRONMENT=development
MOCK_EXTERNAL_APIS=true

# Logging
LOG_LEVEL=DEBUG
SECURITY_LOG_FILE=/app/logs/security.log

# HTTPS settings
HTTPS_ONLY=false

# Frontend URL
FRONTEND_URL=http://localhost:8080

# Rate limiting
RATE_LIMIT_ENABLED=false
RATE_LIMIT_DEFAULT=100/minute
RATE_LIMIT_LOGIN=5/minute

# Email settings
SMTP_SERVER=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_SENDER=noreply@wealthmap.com
SMTP_TLS=true
```

### Frontend Environment Variables

Create a `.env` file in the `frontend` directory with the following variables:

```
VITE_API_URL=http://localhost:8000
VITE_MAPBOX_TOKEN=your_mapbox_token_here
```

## Database Setup

### Using Docker (Recommended)

The Docker Compose configuration automatically sets up PostgreSQL with the required extensions and initializes the database.

### Manual Setup

1. Install PostgreSQL 12 or newer
2. Install the PostGIS extension
3. Create a database named `wealth_map`
4. Create a user `postgres` with password `postgres` (or update the DATABASE_URL environment variable)
5. Grant all privileges on the `wealth_map` database to the user

```sql
CREATE DATABASE wealth_map;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE wealth_map TO postgres;
\c wealth_map
CREATE EXTENSION IF NOT EXISTS postgis;
```

## Development Workflow

### Using Docker

1. Run the setup script: `./setup.sh`
2. Choose the Docker option when prompted
3. Access the services:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PgAdmin: http://localhost:5050 (Email: admin@wealthmap.com, Password: admin)

### Local Development

1. Run the setup script: `./setup.sh`
2. Choose the local development option when prompted
3. Access the services:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Deployment

### Docker Deployment

For production deployment, use the production Docker Compose configuration:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment

#### Backend

1. Set up a production PostgreSQL database
2. Configure environment variables for production
3. Install dependencies: `pip install -r requirements.txt`
4. Run with a production ASGI server:
   ```bash
   gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app
   ```

#### Frontend

1. Build the frontend: `npm run build`
2. Serve the static files with Nginx or another web server

### Important Production Settings

For production deployment, ensure the following:

1. Set `ENVIRONMENT=production` in backend environment
2. Generate a strong, random `SECRET_KEY`
3. Set `HTTPS_ONLY=true`
4. Configure proper `BACKEND_CORS_ORIGINS` with your frontend domain
5. Enable rate limiting: `RATE_LIMIT_ENABLED=true`
6. Set up proper email settings for notifications
7. Configure SSL certificates for HTTPS
8. Set up database backups
9. Configure proper logging and monitoring

## Troubleshooting

### Common Issues

1. **Database connection errors**: Verify PostgreSQL is running and the DATABASE_URL is correct
2. **API key errors**: Ensure all API keys are correctly configured in environment variables
3. **CORS errors**: Check that BACKEND_CORS_ORIGINS includes your frontend URL
4. **Docker memory issues**: Increase memory allocation in Docker settings

For more help, check the logs:
- Backend logs: `backend/logs/`
- Docker logs: `docker-compose logs`