import pytest
from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(backend_dir))

from app.main import app
from app.db.session import get_db
from app.models.user import User, Company, UserActivity
from app.models.token import RefreshToken
from app.core.security import get_password_hash, create_access_token, create_refresh_token

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Create the database tables
    from app.models.user import Base
    Base.metadata.create_all(bind=engine)
    
    # Create a new session for a test
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    # Override the get_db dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test data
    create_test_data(db_session)
    
    # Return test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Remove the override after test
    app.dependency_overrides.clear()

def create_test_data(db_session):
    # Create test company
    company = Company(
        id="11111111-1111-1111-1111-111111111111",
        name="Test Company",
        subscription_tier="premium",
        is_active=True
    )
    db_session.add(company)
    
    # Create regular user
    user = User(
        id="22222222-2222-2222-2222-222222222222",
        email="user@example.com",
        hashed_password=get_password_hash("userpassword"),
        full_name="Test User",
        role="user",
        company_id=company.id,
        is_active=True
    )
    db_session.add(user)
    
    # Create admin user
    admin = User(
        id="33333333-3333-3333-3333-333333333333",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        full_name="Admin User",
        role="admin",
        company_id=company.id,
        is_active=True
    )
    db_session.add(admin)
    
    # Create MFA user
    mfa_user = User(
        id="44444444-4444-4444-4444-444444444444",
        email="mfa@example.com",
        hashed_password=get_password_hash("mfapassword"),
        full_name="MFA User",
        role="user",
        company_id=company.id,
        is_active=True,
        mfa_enabled=True,
        mfa_secret="TESTSECRETKEY"
    )
    db_session.add(mfa_user)
    
    db_session.commit()

@pytest.fixture(scope="function")
def user_token_headers(client):
    login_data = {
        "username": "user@example.com",
        "password": "userpassword",
    }
    response = client.post("/api/auth/login", data=login_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

@pytest.fixture(scope="function")
def admin_token_headers(client):
    login_data = {
        "username": "admin@example.com",
        "password": "adminpassword",
    }
    response = client.post("/api/auth/login", data=login_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}