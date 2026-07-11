"""SQLAlchemy engine, session factory, and declarative base."""

from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path.home() / ".jobs"
BASE_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{BASE_DIR / 'job.db'}"

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def init_db():
    Base.metadata.create_all(engine)
    _add_missing_columns()


NEW_COLUMNS = {
    "created_at": "DATE",
    "response_at": "DATE",
}


def _add_missing_columns():
    """Add columns that were introduced after a user's db file was created."""
    inspector = inspect(engine)
    existing_columns = {col["name"] for col in inspector.get_columns("Entry")}
    with engine.begin() as conn:
        for column, column_type in NEW_COLUMNS.items():
            if column not in existing_columns:
                conn.execute(text(f"ALTER TABLE Entry ADD COLUMN {column} {column_type}"))
