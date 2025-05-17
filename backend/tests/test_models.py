import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.models.user import User, Company, ActivityLog
from app.models.property import Property, Bookmark, Transaction
from app.models.owner import Owner, PropertyOwnership, WealthData
from app.models.search import SavedSearch
from app.models.report import Report

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create the tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    # Drop the tables
    Base.metadata.drop_all(bind=engine)

def test_company_model(db_session):
    """Test creating a company."""
    company = Company(
        id=uuid.uuid4(),
        name="Test Company",
        contact_email="test@example.com",
        subscription_tier="standard",
        max_users=10
    )
    db_session.add(company)
    db_session.commit()
    
    # Query the company
    db_company = db_session.query(Company).filter(Company.name == "Test Company").first()
    assert db_company is not None
    assert db_company.name == "Test Company"
    assert db_company.contact_email == "test@example.com"
    assert db_company.subscription_tier == "standard"
    assert db_company.max_users == 10

def test_user_model(db_session):
    """Test creating a user."""
    # Create a company first
    company_id = uuid.uuid4()
    company = Company(
        id=company_id,
        name="Test Company",
        contact_email="test@example.com"
    )
    db_session.add(company)
    db_session.commit()
    
    # Create a user
    user = User(
        id=uuid.uuid4(),
        email="user@example.com",
        password_hash="hashed_password",
        first_name="Test",
        last_name="User",
        role="standard",
        company_id=company_id
    )
    db_session.add(user)
    db_session.commit()
    
    # Query the user
    db_user = db_session.query(User).filter(User.email == "user@example.com").first()
    assert db_user is not None
    assert db_user.email == "user@example.com"
    assert db_user.first_name == "Test"
    assert db_user.last_name == "User"
    assert db_user.role == "standard"
    assert db_user.company_id == company_id

def test_property_model(db_session):
    """Test creating a property."""
    # Create a property
    property_id = uuid.uuid4()
    property = Property(
        id=property_id,
        address="123 Main St",
        city="New York",
        state="NY",
        zip_code="10001",
        property_type="residential",
        bedrooms=3,
        bathrooms=2.5,
        square_feet=2000,
        location="POINT(40.7128 -74.0060)"  # Simplified for testing
    )
    db_session.add(property)
    db_session.commit()
    
    # Query the property
    db_property = db_session.query(Property).filter(Property.address == "123 Main St").first()
    assert db_property is not None
    assert db_property.address == "123 Main St"
    assert db_property.city == "New York"
    assert db_property.state == "NY"
    assert db_property.zip_code == "10001"
    assert db_property.property_type == "residential"
    assert db_property.bedrooms == 3
    assert db_property.bathrooms == 2.5
    assert db_property.square_feet == 2000

def test_owner_model(db_session):
    """Test creating an owner."""
    # Create an owner
    owner_id = uuid.uuid4()
    owner = Owner(
        id=owner_id,
        name="John Doe",
        owner_type="individual",
        email="john@example.com",
        phone="555-1234"
    )
    db_session.add(owner)
    db_session.commit()
    
    # Query the owner
    db_owner = db_session.query(Owner).filter(Owner.name == "John Doe").first()
    assert db_owner is not None
    assert db_owner.name == "John Doe"
    assert db_owner.owner_type == "individual"
    assert db_owner.email == "john@example.com"
    assert db_owner.phone == "555-1234"

def test_wealth_data_model(db_session):
    """Test creating wealth data for an owner."""
    # Create an owner first
    owner_id = uuid.uuid4()
    owner = Owner(
        id=owner_id,
        name="John Doe",
        owner_type="individual"
    )
    db_session.add(owner)
    db_session.commit()
    
    # Create wealth data
    wealth_data = WealthData(
        id=uuid.uuid4(),
        owner_id=owner_id,
        estimated_net_worth=1000000.00,
        confidence_level=85,
        liquid_assets=250000.00,
        real_estate_assets=500000.00,
        investment_assets=250000.00
    )
    db_session.add(wealth_data)
    db_session.commit()
    
    # Query the wealth data
    db_wealth_data = db_session.query(WealthData).filter(WealthData.owner_id == owner_id).first()
    assert db_wealth_data is not None
    assert db_wealth_data.estimated_net_worth == 1000000.00
    assert db_wealth_data.confidence_level == 85
    assert db_wealth_data.liquid_assets == 250000.00
    assert db_wealth_data.real_estate_assets == 500000.00
    assert db_wealth_data.investment_assets == 250000.00