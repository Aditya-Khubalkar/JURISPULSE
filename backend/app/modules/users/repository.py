from backend.app.database.repository import BaseRepository
from .models import User
class UserRepository(BaseRepository[User]): pass
