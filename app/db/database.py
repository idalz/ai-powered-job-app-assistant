from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# PostgreSQL connection URL
DATABASE_URL = settings.DATABASE_URL

# Create the engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define base model for ORM classes
Base = declarative_base()
