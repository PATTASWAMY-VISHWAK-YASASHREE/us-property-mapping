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