from backend.app.database.repository import BaseRepository
from .models import Document
class DocumentRepository(BaseRepository[Document]): pass
