from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.database.base import Base, TimestampMixin

class Case(Base, TimestampMixin):
    __tablename__ = "cases"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    cnr_number: Mapped[str] = mapped_column(String, unique=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    court_name: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="active")
