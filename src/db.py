"""
Database configuration and setup.

Defines the SQLAlchemy engine, session factory, and base model
used across the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from pathlib import Path

# Base directory of the current file, used to build the database path.

BASE_DIR = Path(__file__).resolve().parent

# SQLite database URL pointing to a local file (job.db).

DATABASE_URL = f"sqlite:///{BASE_DIR / 'job.db'}"

# SQLAlchemy engine responsible for managing database connections.

engine = create_engine(DATABASE_URL, echo=False, future=True)

# Factory for creating new database session instances.

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for all ORM models (used for table definitions).

Base = declarative_base()
