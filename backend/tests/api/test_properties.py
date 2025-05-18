import pytest
from fastapi.testclient import TestClient
import uuid
from datetime import datetime

from app.models.property import Property
from app.models.owner import Owner

@pytest.mark.integration
@pytest.mark.api
@pytest.mark.property
class TestPropertyEndpoints:
    
    def test_get_properties_list(self, client, db_session, admin_token_headers):
        """Test getting a list of properties."""
        # Create test properties
        owner = Owner(
            id=uuid.uuid4(),
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="555-123-4567",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(owner)
        
        for i in range(5):
            property = Property(
                id=uuid.uuid4(),
                address=f"{i+1} Test Street",
                city="Test City",
                state="TS",
                zip_code=f"1000{i}",
                property_type="Single Family",
                bedrooms=3,
                bathrooms=2,
                square_feet=1800,
                year_built=2000,
                lot_size=0.25,
                estimated_value=450000,
                owner_id=owner.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db_session.add(property)
        
        db_session.commit()
        
        # Test endpoint
        response = client.get("/api/properties/", headers=admin_token_headers)
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 5
        assert "total" in data
        assert data["total"] == 5
    
    def test_get_property_by_id(self, client, db_session, admin_token_headers):
        """Test getting a property by ID."""
        # Create test property
        owner = Owner(
            id=uuid.uuid4(),
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            phone="555-987-6543",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(owner)
        
        property_id = uuid.uuid4()
        property = Property(
            id=property_id,
            address="123 Main Street",
            city="Anytown",
            state="AT",
            zip_code="12345",
            property_type="Single Family",
            bedrooms=4,
            bathrooms=3,
            square_feet=2200,
            year_built=2010,
            lot_size=0.3,
            estimated_value=550000,
            owner_id=owner.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(property)
        db_session.commit()
        
        # Test endpoint
        response = client.get(f"/api/properties/{property_id}", headers=admin_token_headers)
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(property_id)
        assert data["address"] == "123 Main Street"
        assert data["city"] == "Anytown"
        assert data["owner_id"] == str(owner.id)
    
    def test_create_property(self, client, db_session, admin_token_headers):
        """Test creating a new property."""
        # Create test owner
        owner_id = uuid.uuid4()
        owner = Owner(
            id=owner_id,
            first_name="Robert",
            last_name="Johnson",
            email="robert@example.com",
            phone="555-555-5555",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(owner)
        db_session.commit()
        
        # Test data
        property_data = {
            "address": "456 Oak Avenue",
            "city": "Newtown",
            "state": "NT",
            "zip_code": "67890",
            "property_type": "Townhouse",
            "bedrooms": 3,
            "bathrooms": 2.5,
            "square_feet": 1950,
            "year_built": 2015,
            "lot_size": 0.15,
            "estimated_value": 425000,
            "owner_id": str(owner_id)
        }
        
        # Test endpoint
        response = client.post("/api/properties/", headers=admin_token_headers, json=property_data)
        
        # Assertions
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["address"] == "456 Oak Avenue"
        assert data["city"] == "Newtown"
        assert data["owner_id"] == str(owner_id)
        
        # Verify property was created in database
        created_property = db_session.query(Property).filter(Property.id == uuid.UUID(data["id"])).first()
        assert created_property is not None
        assert created_property.address == "456 Oak Avenue"
    
    def test_update_property(self, client, db_session, admin_token_headers):
        """Test updating a property."""
        # Create test property
        owner = Owner(
            id=uuid.uuid4(),
            first_name="Michael",
            last_name="Brown",
            email="michael@example.com",
            phone="555-111-2222",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(owner)
        
        property_id = uuid.uuid4()
        property = Property(
            id=property_id,
            address="789 Pine Street",
            city="Oldtown",
            state="OT",
            zip_code="54321",
            property_type="Condo",
            bedrooms=2,
            bathrooms=2,
            square_feet=1200,
            year_built=2005,
            lot_size=0.1,
            estimated_value=350000,
            owner_id=owner.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(property)
        db_session.commit()
        
        # Test data
        update_data = {
            "address": "789 Pine Street",
            "city": "Oldtown",
            "state": "OT",
            "zip_code": "54321",
            "property_type": "Condo",
            "bedrooms": 2,
            "bathrooms": 2,
            "square_feet": 1300,  # Updated
            "year_built": 2005,
            "lot_size": 0.1,
            "estimated_value": 375000,  # Updated
            "owner_id": str(owner.id)
        }
        
        # Test endpoint
        response = client.put(f"/api/properties/{property_id}", headers=admin_token_headers, json=update_data)
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(property_id)
        assert data["square_feet"] == 1300
        assert data["estimated_value"] == 375000
        
        # Verify property was updated in database
        updated_property = db_session.query(Property).filter(Property.id == property_id).first()
        assert updated_property.square_feet == 1300
        assert updated_property.estimated_value == 375000
    
    def test_delete_property(self, client, db_session, admin_token_headers):
        """Test deleting a property."""
        # Create test property
        owner = Owner(
            id=uuid.uuid4(),
            first_name="Sarah",
            last_name="Wilson",
            email="sarah@example.com",
            phone="555-333-4444",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(owner)
        
        property_id = uuid.uuid4()
        property = Property(
            id=property_id,
            address="321 Elm Road",
            city="Sometown",
            state="ST",
            zip_code="13579",
            property_type="Single Family",
            bedrooms=3,
            bathrooms=2,
            square_feet=1700,
            year_built=1995,
            lot_size=0.2,
            estimated_value=400000,
            owner_id=owner.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db_session.add(property)
        db_session.commit()
        
        # Test endpoint
        response = client.delete(f"/api/properties/{property_id}", headers=admin_token_headers)
        
        # Assertions
        assert response.status_code == 204
        
        # Verify property was deleted from database
        deleted_property = db_session.query(Property).filter(Property.id == property_id).first()
        assert deleted_property is None
    
    def test_unauthorized_access(self, client, db_session):
        """Test unauthorized access to property endpoints."""
        # Test without authentication
        response = client.get("/api/properties/")
        assert response.status_code == 401
        
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/properties/", headers=headers)
        assert response.status_code == 401