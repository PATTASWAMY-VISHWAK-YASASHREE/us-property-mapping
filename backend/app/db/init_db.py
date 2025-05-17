from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import Base, engine
from app.models.user import User

# Create tables
def init_db() -> None:
    Base.metadata.create_all(bind=engine)

# Create initial admin user
def create_initial_admin(db: Session) -> None:
    admin = db.query(User).filter(User.email == "admin@wealthmap.com").first()
    if not admin:
        admin_user = User(
            email="admin@wealthmap.com",
            hashed_password=get_password_hash("admin"),
            full_name="Admin User",
            is_admin=True,
            is_active=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)