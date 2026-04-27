"""SQLAlchemy engine, session factory, and declarative base."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = f"sqlite:///{BASE_DIR / 'job.db'}"

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def init_db():
    Base.metadata.create_all(engine)
