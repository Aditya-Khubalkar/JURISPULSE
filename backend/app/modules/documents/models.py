from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.database.base import Base, TimestampMixin

class Document(Base, TimestampMixin):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    file_name: Mapped[str] = mapped_column(String)
    storage_path: Mapped[str] = mapped_column(String)
    ocr_status: Mapped[str] = mapped_column(String, default="completed")
