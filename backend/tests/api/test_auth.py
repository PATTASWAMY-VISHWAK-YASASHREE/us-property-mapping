import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timedelta

from app.main import app
from app.core.config import settings
from app.models.user import User, Company
from app.models.token import RefreshToken
from app.core.security import get_password_hash, create_access_token, create_refresh_token
from app.services.token import TokenService

client = TestClient(app)

@pytest.fixture
def db_session(monkeypatch):
    """
    Mock database session for testing
    """
    class MockSession:
        def __init__(self):
            self.committed = False
            self.closed = False
            self.users = {}
            self.companies = {}
            self.refresh_tokens = {}
            self.token_blacklist = {}
            
        def add(self, obj):
            if isinstance(obj, User):
                self.users[obj.id] = obj
            elif isinstance(obj, Company):
                self.companies[obj.id] = obj
            elif isinstance(obj, RefreshToken):
                self.refresh_tokens[obj.id] = obj
                
        def commit(self):
            self.committed = True
            
        def close(self):
            self.closed = True
            
        def query(self, model):
            return MockQuery(self, model)
            
        def flush(self):
            pass
            
        def refresh(self, obj):
            pass
    
    class MockQuery:
        def __init__(self, session, model):
            self.session = session
            self.model = model
            self.filters = []
            
        def filter(self, *args):
            self.filters.extend(args)
            return self
            
        def first(self):
            if self.model == User:
                for user in self.session.users.values():
                    for f in self.filters:
                        if "email" in str(f) and user.email in str(f):
                            return user
            return None
            
        def delete(self):
            return 0
    
    mock_session = MockSession()
    
    # Create a test company
    company = Company(
        id=uuid.uuid4(),
        name="Test Company",
        contact_email="admin@example.com"
    )
    mock_session.add(company)
    
    # Create a test user
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        first_name="Test",
        last_name="User",
        role="admin",
        is_active=True,
        company_id=company.id,
        mfa_enabled=False
    )
    mock_session.add(user)
    
    # Create a user with MFA enabled
    mfa_user = User(
        id=uuid.uuid4(),
        email="mfa@example.com",
        password_hash=get_password_hash("password123"),
        first_name="MFA",
        last_name="User",
        role="admin",
        is_active=True,
        company_id=company.id,
        mfa_enabled=True,
        mfa_secret="encrypted:testsecret"
    )
    mock_session.add(mfa_user)
    
    def mock_get_db():
        return mock_session
        
    def mock_create_tokens(user_id, db):
        access_token = create_access_token(subject=str(user_id))
        refresh_token, jti = create_refresh_token(subject=str(user_id))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    # Apply the monkeypatches
    monkeypatch.setattr("app.core.dependencies.get_db", mock_get_db)
    monkeypatch.setattr("app.api.auth.get_db", mock_get_db)
    monkeypatch.setattr("app.services.token.TokenService.create_tokens", mock_create_tokens)
    
    return mock_session

def test_login_success(db_session):
    """Test successful login"""
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(db_session):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()

def test_login_mfa_required(db_session):
    """Test login with MFA enabled"""
    response = client.post(
        "/api/auth/login",
        data={"username": "mfa@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data.get("mfa_required") is True

def test_register_company(db_session):
    """Test company registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "company_name": "New Company",
            "admin_email": "new@example.com",
            "admin_password": "securepassword",
            "admin_full_name": "New Admin"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_register_existing_email(db_session):
    """Test registration with existing email"""
    response = client.post(
        "/api/auth/register",
        json={
            "company_name": "New Company",
            "admin_email": "test@example.com",  # Already exists
            "admin_password": "securepassword",
            "admin_full_name": "New Admin"
        }
    )
    assert response.status_code == 400
    assert "detail" in response.json()

# Add more tests for refresh token, logout, MFA, etc.