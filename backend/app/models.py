from sqlalchemy import Boolean, DateTime, Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    session_key: Mapped[int] = mapped_column(Integer, primary_key=True)
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

    # Keep the original API record for future analysis.
    raw_data: Mapped[dict] = mapped_column(JSON)


class DriverModel(Base):
    __tablename__ = "drivers"

    # Driver numbers can be reused across sessions/seasons.
    session_key: Mapped[int] = mapped_column(Integer, primary_key=True)
    driver_number: Mapped[int] = mapped_column(Integer, primary_key=True)

    meeting_key: Mapped[int] = mapped_column(Integer, nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    name_acronym: Mapped[str] = mapped_column(String(10), nullable=True)
    team_name: Mapped[str] = mapped_column(String(100), nullable=True)
    team_colour: Mapped[str] = mapped_column(String(10), nullable=True)
    headshot_url: Mapped[str] = mapped_column(String(500), nullable=True)

    raw_data: Mapped[dict] = mapped_column(JSON)


class LapModel(Base):
    __tablename__ = "laps"

    # One lap per driver, per session.
    session_key: Mapped[int] = mapped_column(Integer, primary_key=True)
    driver_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    lap_number: Mapped[int] = mapped_column(Integer, primary_key=True)

    meeting_key: Mapped[int] = mapped_column(Integer, nullable=True)
    date_start: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)

    lap_duration: Mapped[float] = mapped_column(Float, nullable=True)
    duration_sector_1: Mapped[float] = mapped_column(Float, nullable=True)
    duration_sector_2: Mapped[float] = mapped_column(Float, nullable=True)
    duration_sector_3: Mapped[float] = mapped_column(Float, nullable=True)

    i1_speed: Mapped[int] = mapped_column(Integer, nullable=True)
    i2_speed: Mapped[int] = mapped_column(Integer, nullable=True)
    st_speed: Mapped[int] = mapped_column(Integer, nullable=True)

    is_pit_out_lap: Mapped[bool] = mapped_column(Boolean, nullable=True)

    # Preserve the complete API response, including sector segments.
    raw_data: Mapped[dict] = mapped_column(JSON)