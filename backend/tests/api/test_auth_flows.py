import pytest
from fastapi.testclient import TestClient
import uuid
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from app.models.user import User, Company
from app.models.token import RefreshToken
from app.core.security import get_password_hash, create_access_token, create_refresh_token

@pytest.mark.integration
@pytest.mark.api
@pytest.mark.auth
class TestAuthFlows:
    
    def test_complete_login_flow(self, client, db_session):
        """Test the complete login flow including token refresh."""
        # Step 1: Login with valid credentials
        login_data = {
            "username": "user@example.com",
            "password": "userpassword",
        }
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == 200
        tokens = response.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "bearer"
        
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        
        # Step 2: Access protected endpoint with access token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/users/me", headers=headers)
        
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["email"] == "user@example.com"
        
        # Step 3: Refresh the token
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/api/auth/refresh", json=refresh_data)
        
        assert response.status_code == 200
        new_tokens = response.json()
        assert "access_token" in new_tokens
        assert "refresh_token" in new_tokens
        assert new_tokens["access_token"] != access_token
        
        # Step 4: Access protected endpoint with new access token
        headers = {"Authorization": f"Bearer {new_tokens['access_token']}"}
        response = client.get("/api/users/me", headers=headers)
        
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["email"] == "user@example.com"
        
        # Step 5: Logout
        response = client.post("/api/auth/logout", json={"refresh_token": new_tokens["refresh_token"]}, headers=headers)
        
        assert response.status_code == 200
        
        # Step 6: Verify old token no longer works
        response = client.get("/api/users/me", headers=headers)
        assert response.status_code == 401
    
    def test_mfa_flow(self, client, db_session):
        """Test the MFA authentication flow."""
        # Mock the TOTP verification
        with patch('app.api.auth.verify_totp') as mock_verify_totp:
            mock_verify_totp.return_value = True
            
            # Step 1: Login with MFA user
            login_data = {
                "username": "mfa@example.com",
                "password": "mfapassword",
            }
            response = client.post("/api/auth/login", data=login_data)
            
            assert response.status_code == 200
            tokens = response.json()
            assert "access_token" in tokens
            assert tokens.get("mfa_required") is True
            
            # This is a limited access token
            limited_token = tokens["access_token"]
            
            # Step 2: Try to access protected endpoint with limited token
            headers = {"Authorization": f"Bearer {limited_token}"}
            response = client.get("/api/users/me", headers=headers)
            
            # Should fail because MFA is not completed
            assert response.status_code == 403
            
            # Step 3: Complete MFA verification
            mfa_data = {"mfa_code": "123456"}
            response = client.post("/api/auth/verify-mfa", json=mfa_data, headers=headers)
            
            assert response.status_code == 200
            full_tokens = response.json()
            assert "access_token" in full_tokens
            assert "refresh_token" in full_tokens
            
            # Step 4: Access protected endpoint with full access token
            headers = {"Authorization": f"Bearer {full_tokens['access_token']}"}
            response = client.get("/api/users/me", headers=headers)
            
            assert response.status_code == 200
            user_data = response.json()
            assert user_data["email"] == "mfa@example.com"
    
    def test_password_reset_flow(self, client, db_session):
        """Test the password reset flow."""
        # Mock the email sending function
        with patch('app.services.email.EmailService.send_password_reset') as mock_send_email:
            # Step 1: Request password reset
            reset_data = {"email": "user@example.com"}
            response = client.post("/api/auth/forgot-password", json=reset_data)
            
            assert response.status_code == 200
            assert mock_send_email.called
            
            # Extract the reset token from the mock call
            # In a real test, we'd need to extract this from the database
            # Here we'll create a token manually
            user = db_session.query(User).filter(User.email == "user@example.com").first()
            reset_token = create_access_token(
                subject=str(user.id),
                expires_delta=timedelta(minutes=30),
                scopes=["password-reset"]
            )
            
            # Step 2: Reset password with token
            new_password_data = {
                "token": reset_token,
                "new_password": "newpassword123"
            }
            response = client.post("/api/auth/reset-password", json=new_password_data)
            
            assert response.status_code == 200
            
            # Step 3: Login with new password
            login_data = {
                "username": "user@example.com",
                "password": "newpassword123",
            }
            response = client.post("/api/auth/login", data=login_data)
            
            assert response.status_code == 200
            tokens = response.json()
            assert "access_token" in tokens
    
    def test_registration_flow(self, client, db_session):
        """Test the user registration flow."""
        # Step 1: Register a new company and admin user
        register_data = {
            "company_name": "New Test Company",
            "admin_email": "newadmin@example.com",
            "admin_password": "securepassword123",
            "admin_full_name": "New Admin User"
        }
        response = client.post("/api/auth/register", json=register_data)
        
        assert response.status_code == 200
        tokens = response.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        
        # Step 2: Verify the company and user were created
        company = db_session.query(Company).filter(Company.name == "New Test Company").first()
        assert company is not None
        
        user = db_session.query(User).filter(User.email == "newadmin@example.com").first()
        assert user is not None
        assert user.role == "admin"
        assert user.company_id == company.id
        
        # Step 3: Login with the new user
        login_data = {
            "username": "newadmin@example.com",
            "password": "securepassword123",
        }
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == 200
        tokens = response.json()
        assert "access_token" in tokens
    
    def test_role_based_access_control(self, client, db_session, admin_token_headers, user_token_headers):
        """Test role-based access control."""
        # Admin should be able to access admin endpoints
        response = client.get("/api/admin/users", headers=admin_token_headers)
        assert response.status_code == 200
        
        # Regular user should not be able to access admin endpoints
        response = client.get("/api/admin/users", headers=user_token_headers)
        assert response.status_code == 403
        
        # Both admin and regular user should be able to access user endpoints
        response = client.get("/api/users/me", headers=admin_token_headers)
        assert response.status_code == 200
        
        response = client.get("/api/users/me", headers=user_token_headers)
        assert response.status_code == 200
    
    def test_token_expiration(self, client, db_session):
        """Test token expiration handling."""
        # Create a user
        user = db_session.query(User).filter(User.email == "user@example.com").first()
        
        # Create an expired token
        expired_token = create_access_token(
            subject=str(user.id),
            expires_delta=timedelta(minutes=-30)  # Negative value to make it expired
        )
        
        # Try to use the expired token
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/api/users/me", headers=headers)
        
        # Should fail with 401 Unauthorized
        assert response.status_code == 401
        assert "token" in response.json()["detail"].lower()
        assert "expired" in response.json()["detail"].lower()
    
    def test_invalid_token(self, client, db_session):
        """Test handling of invalid tokens."""
        # Try to use an invalid token
        headers = {"Authorization": "Bearer invalid_token_format"}
        response = client.get("/api/users/me", headers=headers)
        
        # Should fail with 401 Unauthorized
        assert response.status_code == 401
        
        # Try to use a token with invalid signature
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"}
        response = client.get("/api/users/me", headers=headers)
        
        # Should fail with 401 Unauthorized
        assert response.status_code == 401