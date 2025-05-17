# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.session import Base
from app.models.user import User
from app.models.property import Property
from app.models.owner import Owner
from app.models.bookmark import Bookmark
from app.models.search import SavedSearch
from app.models.report import Report