import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    async def send_email(
        recipient_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send an email using the configured SMTP server
        """
        # In development mode, just log the email
        if settings.ENVIRONMENT == "development" and not settings.SMTP_SERVER:
            logger.info(f"Would send email to {recipient_email} with subject: {subject}")
            logger.info(f"Content: {html_content}")
            return True
            
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = settings.SMTP_SENDER
            message["To"] = recipient_email
            
            # Add text content if provided, otherwise use a simple version of the HTML
            if text_content:
                message.attach(MIMEText(text_content, "plain"))
            else:
                # Create a simple text version from HTML
                simple_text = html_content.replace("<br>", "\n").replace("</p>", "\n").replace("<li>", "- ")
                # Remove all other HTML tags
                import re
                simple_text = re.sub(r'<[^>]*>', '', simple_text)
                message.attach(MIMEText(simple_text, "plain"))
                
            # Add HTML content
            message.attach(MIMEText(html_content, "html"))
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_SENDER, recipient_email, message.as_string())
                
            logger.info(f"Email sent to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            return False
    
    @staticmethod
    async def send_user_invitation(
        recipient_email: str,
        company_name: str,
        invitation_link: str,
        inviter_name: str
    ) -> bool:
        """
        Send an invitation email to a new user
        """
        subject = f"Invitation to join {company_name} on Wealth Map"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4a6cf7; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ display: inline-block; background-color: #4a6cf7; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 4px; margin-top: 20px; }}
                .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>You've been invited!</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>{inviter_name} has invited you to join <strong>{company_name}</strong> on the Wealth Map platform.</p>
                    <p>Wealth Map is a powerful tool for property analysis and wealth management.</p>
                    <p>To accept this invitation and create your account, please click the button below:</p>
                    <p style="text-align: center;">
                        <a href="{invitation_link}" class="button">Accept Invitation</a>
                    </p>
                    <p>This invitation link will expire in 7 days.</p>
                    <p>If you have any questions, please contact {inviter_name} directly.</p>
                    <p>Best regards,<br>The Wealth Map Team</p>
                </div>
                <div class="footer">
                    <p>If you received this email by mistake, please ignore it.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await EmailService.send_email(recipient_email, subject, html_content)
    
    @staticmethod
    async def send_password_reset(
        recipient_email: str,
        reset_link: str
    ) -> bool:
        """
        Send a password reset email
        """
        subject = "Reset Your Wealth Map Password"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4a6cf7; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ display: inline-block; background-color: #4a6cf7; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 4px; margin-top: 20px; }}
                .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Reset Request</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>We received a request to reset your password for your Wealth Map account.</p>
                    <p>To reset your password, please click the button below:</p>
                    <p style="text-align: center;">
                        <a href="{reset_link}" class="button">Reset Password</a>
                    </p>
                    <p>This link will expire in 24 hours.</p>
                    <p>If you didn't request a password reset, please ignore this email or contact support if you have concerns.</p>
                    <p>Best regards,<br>The Wealth Map Team</p>
                </div>
                <div class="footer">
                    <p>If you received this email by mistake, please ignore it.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await EmailService.send_email(recipient_email, subject, html_content)
    
    @staticmethod
    async def send_email_verification(
        recipient_email: str,
        verification_link: str
    ) -> bool:
        """
        Send an email verification link
        """
        subject = "Verify Your Wealth Map Email Address"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4a6cf7; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ display: inline-block; background-color: #4a6cf7; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 4px; margin-top: 20px; }}
                .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Verify Your Email</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>Thank you for registering with Wealth Map. To complete your registration, please verify your email address by clicking the button below:</p>
                    <p style="text-align: center;">
                        <a href="{verification_link}" class="button">Verify Email</a>
                    </p>
                    <p>This link will expire in 24 hours.</p>
                    <p>If you didn't create an account with Wealth Map, please ignore this email.</p>
                    <p>Best regards,<br>The Wealth Map Team</p>
                </div>
                <div class="footer">
                    <p>If you received this email by mistake, please ignore it.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await EmailService.send_email(recipient_email, subject, html_content)