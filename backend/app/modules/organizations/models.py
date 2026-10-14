from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.database.base import Base
class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
