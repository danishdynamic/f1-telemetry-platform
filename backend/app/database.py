
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings


# Build the database URL safely from individual settings.
# SQLAlchemy handles special characters in the password.
from sqlalchemy.engine import URL

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.database_user,
    password=settings.database_password,
    host=settings.database_host,
    port=settings.database_port,
    database=settings.database_name,
)


# Engine manages connections between Python and PostgreSQL.
engine = create_engine(
    database_url,
    pool_pre_ping=True,
)


# Each request can get its own database session.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base class for future database models.
class Base(DeclarativeBase):
    pass


def get_db():
    # Create a session when an API request needs the database.
    db = SessionLocal()

    try:
        yield db
    finally:
        # Always release the connection after the request.
        db.close()
