"""
Tests for the API layer (EntryDB).

These tests validate:
- CRUD operations
- Business rule enforcement
- Error handling and exceptions
- Interaction with the database session
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api import EntryDB
from src.db import Base
from src.exceptions import EntryException


@pytest.fixture
def session():
    """Creates an in-memory SQLite session for testing."""
    # setup
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # yield
    try:
        # Provide the database interface to the caller.
        yield session
    # teardown
    finally:
        # Always close the session to release resources.
        session.rollback()
        session.close()


@pytest.fixture
def database_api(session):
    return EntryDB(session)


# --------------------CREATE--------------------#
@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {"company": "Github", "job_title": "Python Dev"},
            {
                "id": 1,
                "company": "Github",
                "job_title": "Python Dev",
                "status": "Pending start",
            },
        ),
        (
            {"company": "Microsoft", "job_title": "Data Analyst", "status": "Accepted"},
            {
                "id": 1,
                "company": "Microsoft",
                "job_title": "Data Analyst",
                "status": "Accepted",
            },
        ),
    ],
)
def test_valid_entry_insert(data, expected, database_api):
    database_api.add(data)
    entries = database_api.get_all()
    entry = entries[0]

    assert len(entries) == 1

    for field, expected_value in expected.items():
        assert entry[field] == expected_value


@pytest.mark.parametrize(
    "data",
    [
        {"company": "Github", "job_title": "      "},
        {"company": "Microsoft", "job_title": "", "status": "Accepted"},
        {"company": "", "job_title": "Data Analyst"},
        {"company": "   ", "job_title": "Devops", "status": "Rejected"},
        {"company": "  ", "job_title": "  ", "status": "Unknown"},
    ],
)
def test_missing_field(data, database_api):
    with pytest.raises(EntryException):
        database_api.add(data)


@pytest.mark.parametrize(
    "data",
    [
        {"company": "Github", "job_title": True},
        {"company": 1, "job_title": "Python Dev", "status": "Accepted"},
        {"company": True, "job_title": "Data Analyst"},
        {"company": "Apple", "job_title": 1, "status": False},
        {"company": False, "job_title": -9, "status": 1},
    ],
)
def test_invalid_field_type(data, database_api):
    with pytest.raises(EntryException):
        database_api.add(data)
