from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.database.base import Base, TimestampMixin
class Hearing(Base, TimestampMixin):
    __tablename__ = "hearings"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    case_id: Mapped[str] = mapped_column(String)
    hearing_date: Mapped[str] = mapped_column(String)
    courtroom: Mapped[str] = mapped_column(String)
