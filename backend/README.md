# Wealth Map Backend

This is the backend service for the Wealth Map platform, built with FastAPI and PostgreSQL.

## Database Schema

The database schema has been updated to use UUID primary keys and includes the following tables:

- `companies`: Stores company information for multi-tenant support
- `users`: Stores user information with company association
- `properties`: Stores property details with geospatial data
- `owners`: Stores property owner information
- `property_ownership`: Tracks ownership relationships between properties and owners
- `wealth_data`: Stores wealth-related data for owners
- `transactions`: Records property transactions
- `saved_searches`: Stores user-saved search criteria
- `bookmarks`: Tracks user-bookmarked properties
- `reports`: Stores report configurations
- `activity_logs`: Tracks user activity in the system
- `property_mappings`: Maps internal property IDs to external property IDs (e.g., Zillow)

## Third-Party API Integrations

### Zillow API Integration

The platform integrates with Zillow's API through RapidAPI to provide property data, valuations, and market insights.

#### Setup Requirements

1. Register for a [RapidAPI account](https://rapidapi.com/auth/sign-up)
2. Subscribe to the [Zillow API on RapidAPI](https://rapidapi.com/apimaker/api/zillow-com1/)
3. Retrieve your API key and configure it in the environment variables

#### Available Zillow API Endpoints

- `/api/properties/zillow/search` - Property lookup by address
- `/api/properties/zillow/zestimate/{zpid}` - Property valuation data
- `/api/properties/zillow/comps/{zpid}` - Comparable properties
- `/api/properties/zillow/deep-comps/{zpid}` - Detailed comparable properties
- `/api/properties/zillow/details/{zpid}` - Enhanced property information
- `/api/properties/zillow/demographics/{region_id}` - Neighborhood demographics
- `/api/properties/zillow/region-children/{region_id}` - Geographic hierarchy information
- `/api/properties/zillow/map-property` - Map Zillow property IDs to internal property IDs

#### Environment Variables for Zillow API

```
RAPIDAPI_KEY=your_rapidapi_key_here
ZILLOW_API_HOST=zillow-com1.p.rapidapi.com
ZILLOW_CACHE_EXPIRY=3600
ZILLOW_MAX_RETRIES=3
ZILLOW_RETRY_DELAY=2
ZILLOW_IMAGE_STORAGE_PATH=/tmp/property_images
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+ with PostGIS extension
- Docker (optional)

### Local Development Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   export DATABASE_URL=postgresql://user:password@localhost:5432/wealthmap
   export RAPIDAPI_KEY=your_rapidapi_key_here
   ```

4. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

### Database Initialization

The database will be automatically initialized when the application starts. This includes:

1. Running SQL migrations from the `app/db/migrations` directory
2. Creating database tables based on SQLAlchemy models
3. Creating an initial admin user

You can also manually run migrations:

```
python -m app.db.run_migrations
```

## Testing

Run tests with pytest:

```
pytest
```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Deployment

Build and run with Docker Compose:

```
docker-compose up -d
```