"""
Test database connection to ensure it's properly configured.
"""
import os
import pytest
import sqlalchemy
from sqlalchemy import text

def test_database_connection():
    """Test that we can connect to the database with the correct credentials."""
    # Get the database URL from environment variable or use default
    db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:vishwak@localhost:5432/wealth_map")
    
    # Create engine
    engine = sqlalchemy.create_engine(db_url)
    
    try:
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1
            print("Database connection successful!")
            
            # Try to query the db_info table if it exists
            try:
                result = connection.execute(text("SELECT message FROM db_info LIMIT 1"))
                message = result.scalar()
                print(f"Database info message: {message}")
                assert "EDB PostgreSQL server up and running" in message
                assert "wealth_map" in message
                assert "vishwak" in message
            except:
                print("db_info table not found, but connection is working")
                pass
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")