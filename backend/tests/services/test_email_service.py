import pytest
from unittest.mock import patch, MagicMock
from app.services.email import EmailService
from app.core.config import settings

class TestEmailService:
    """Tests for the EmailService class."""
    
    @pytest.mark.asyncio
    async def test_email_configuration(self):
        """Test that the email configuration is correctly set."""
        assert settings.SMTP_SERVER == "smtp.gmail.com"
        assert settings.SMTP_PORT == 587
        assert settings.SMTP_USERNAME == "pvishwak18@gmail.com"
        assert settings.SMTP_SENDER == "pvishwak18@gmail.com"
        assert settings.SMTP_TLS is True
    
    @pytest.mark.asyncio
    async def test_send_email(self):
        """Test sending an email with mocked SMTP."""
        with patch('smtplib.SMTP') as mock_smtp:
            # Configure the mock
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            # Call the send_email method
            result = await EmailService.send_email(
                recipient_email="test@example.com",
                subject="Test Email",
                html_content="<p>This is a test email.</p>"
            )
            
            # Verify the result and SMTP calls
            assert result is True
            mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with("pvishwak18@gmail.com", settings.SMTP_PASSWORD)
            mock_server.sendmail.assert_called_once()
            
            # Verify the email parameters
            call_args = mock_server.sendmail.call_args[0]
            assert call_args[0] == "pvishwak18@gmail.com"  # From
            assert call_args[1] == "test@example.com"      # To
            
    @pytest.mark.asyncio
    async def test_send_user_invitation(self):
        """Test sending a user invitation email."""
        with patch.object(EmailService, 'send_email', return_value=True) as mock_send:
            result = await EmailService.send_user_invitation(
                recipient_email="new@example.com",
                company_name="Test Company",
                invitation_link="https://example.com/invite/123",
                inviter_name="Test Admin"
            )
            
            assert result is True
            mock_send.assert_called_once()
            
            # Verify the email parameters
            call_args = mock_send.call_args[0]
            assert call_args[0] == "new@example.com"
            assert "Invitation to join Test Company" in call_args[1]
            assert "Test Admin has invited you" in call_args[2]
            
    @pytest.mark.asyncio
    async def test_send_password_reset(self):
        """Test sending a password reset email."""
        with patch.object(EmailService, 'send_email', return_value=True) as mock_send:
            result = await EmailService.send_password_reset(
                recipient_email="user@example.com",
                reset_link="https://example.com/reset/123"
            )
            
            assert result is True
            mock_send.assert_called_once()
            
            # Verify the email parameters
            call_args = mock_send.call_args[0]
            assert call_args[0] == "user@example.com"
            assert "Reset Your Wealth Map Password" in call_args[1]
            assert "https://example.com/reset/123" in call_args[2]
            
    @pytest.mark.asyncio
    async def test_send_email_verification(self):
        """Test sending an email verification email."""
        with patch.object(EmailService, 'send_email', return_value=True) as mock_send:
            result = await EmailService.send_email_verification(
                recipient_email="new@example.com",
                verification_link="https://example.com/verify/123"
            )
            
            assert result is True
            mock_send.assert_called_once()
            
            # Verify the email parameters
            call_args = mock_send.call_args[0]
            assert call_args[0] == "new@example.com"
            assert "Verify Your Wealth Map Email" in call_args[1]
            assert "https://example.com/verify/123" in call_args[2]