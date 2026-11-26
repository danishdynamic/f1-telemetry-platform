
from sqlalchemy import Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SessionModel(Base):
    # This Python class represents a PostgreSQL table.
    __tablename__ = "sessions"

    # OpenF1 session_key uniquely identifies a session.
    session_key: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    meeting_key: Mapped[int] = mapped_column(Integer, index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)

    session_name: Mapped[str] = mapped_column(String(100))
    session_type: Mapped[str] = mapped_column(String(50))

    date_start: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    date_end: Mapped[DateTime] = mapped_column(DateTime(timezone=True))

    circuit_key: Mapped[int] = mapped_column(Integer)
    circuit_short_name: Mapped[str] = mapped_column(String(100))

    country_name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))

    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)

    # Store the complete original API response as JSON.
    raw_data: Mapped[dict] = mapped_column(JSON)
