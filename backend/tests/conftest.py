import pytest
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(backend_dir))
os.environ["PYTHONPATH"] = str(backend_dir)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings
from app.models.user import User, Company
from app.core.security import get_password_hash
import uuid
from datetime import datetime, timedelta

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Creates a new database session for each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    
    # Create a session bound to the connection
    Session = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = Session()
    
    # Create test data
    # Create a test company
    company = Company(
        id=uuid.uuid4(),
        name="Test Company",
        contact_email="admin@example.com",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(company)
    
    # Create a test admin user
    admin_user = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        password_hash=get_password_hash("adminpassword"),
        first_name="Admin",
        last_name="User",
        role="admin",
        is_active=True,
        company_id=company.id,
        mfa_enabled=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(admin_user)
    
    # Create a test regular user
    regular_user = User(
        id=uuid.uuid4(),
        email="user@example.com",
        password_hash=get_password_hash("userpassword"),
        first_name="Regular",
        last_name="User",
        role="user",
        is_active=True,
        company_id=company.id,
        mfa_enabled=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(regular_user)
    
    # Create a test user with MFA enabled
    mfa_user = User(
        id=uuid.uuid4(),
        email="mfa@example.com",
        password_hash=get_password_hash("mfapassword"),
        first_name="MFA",
        last_name="User",
        role="user",
        is_active=True,
        company_id=company.id,
        mfa_enabled=True,
        mfa_secret="encrypted:testsecret",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(mfa_user)
    
    session.commit()
    
    # Override the get_db dependency to use our test database
    def override_get_db():
        try:
            yield session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield session
    
    # Rollback the transaction and close the connection
    transaction.rollback()
    connection.close()
    
    # Remove the dependency override
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def client(db_session):
    """Creates a test client using the test database."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def admin_token_headers(client):
    """Returns authorization headers for admin user."""
    login_data = {
        "username": "admin@example.com",
        "password": "adminpassword",
    }
    response = client.post("/api/auth/login", data=login_data)
    tokens = response.json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    return headers

@pytest.fixture(scope="function")
def user_token_headers(client):
    """Returns authorization headers for regular user."""
    login_data = {
        "username": "user@example.com",
        "password": "userpassword",
    }
    response = client.post("/api/auth/login", data=login_data)
    tokens = response.json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    return headers