from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


# Define base model for ORM classes (SQLAlchemy 2.0 style)
class Base(DeclarativeBase):
    pass


# PostgreSQL connection URL (psycopg3 format)
DATABASE_URL = settings.DATABASE_URL

# Create the engine with psycopg3
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging during development
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
