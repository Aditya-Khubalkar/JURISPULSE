from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.database.base import Base
class Role(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    permissions: Mapped[list] = mapped_column(JSON, default=list)
