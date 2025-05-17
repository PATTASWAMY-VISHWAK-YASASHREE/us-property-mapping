import uuid
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import Base, engine
from app.models.user import User, Company

# Create tables
def init_db() -> None:
    Base.metadata.create_all(bind=engine)

# Create initial admin user and company
def create_initial_admin(db: Session) -> None:
    admin = db.query(User).filter(User.email == "admin@wealthmap.com").first()
    if not admin:
        # Create default company first
        company = Company(
            id=uuid.uuid4(),
            name="Wealth Map Admin",
            contact_email="admin@wealthmap.com",
            subscription_tier="enterprise",
            max_users=100
        )
        db.add(company)
        db.flush()  # Flush to get the company ID
        
        # Create admin user
        admin_user = User(
            id=uuid.uuid4(),
            email="admin@wealthmap.com",
            password_hash=get_password_hash("admin"),
            first_name="Admin",
            last_name="User",
            role="admin",
            is_active=True,
            company_id=company.id
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)