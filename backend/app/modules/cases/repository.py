from backend.app.database.repository import BaseRepository
from .models import Case
class CaseRepository(BaseRepository[Case]): pass
