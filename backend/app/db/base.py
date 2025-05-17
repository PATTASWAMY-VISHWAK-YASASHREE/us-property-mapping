# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.session import Base
from app.models.user import User, Company, ActivityLog
from app.models.property import Property, Bookmark, Transaction
from app.models.owner import Owner, PropertyOwnership, WealthData
from app.models.search import SavedSearch
from app.models.report import Report
from app.models.property_mapping import PropertyMapping