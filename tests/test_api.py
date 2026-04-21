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
from tests.data.entry_data import (
    VALID_ENTRIES,
    MISSING_FIELD_ENTRIES,
    INVALID_FIELD_ENTRIES,
    INSERT_COUNTS,
    ENTRY_GENERATOR_COUNT,
)
from tests.data.get_by_cases import (
    INVALID_ID_GET_BY,
    SINGLE_CONDITION_GET_BY,
    MULTIPLE_CONDITION_GET_BY,
    GET_BY_NO_MATCH,
    INVALID_FIELD_GET_BY,
)
from tests.data.update_cases import (
    FULL_UPDATE,
    PARTIAL_UPDATE,
    INVALID_UPDATE_PAYLOADS,
)
from tests.data.delete_cases import (
    DELETE_VALID_ID_CASES,
    DELETE_INVALID_ID_CASES,
    DELETE_ALL_CASES,
)


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


def entry_data_generator(i):
    companies = ["Github", "Microsoft", "Apple", "Amazon", "Netflix", "Meta"]
    jobs = ["Data Engineer", "DevOps", "ML Engineer", "Python Dev", "QA Developer"]

    return {"company": companies[i % len(companies)], "job_title": jobs[i % len(jobs)]}


# Helper to generate deterministic test data for bulk operations.
# Uses modulo to cycle through predefined values for consistency.


# --------------------CREATE--------------------#
# Validates that a correct payload is inserted and persisted accurately.
@pytest.mark.create
@pytest.mark.parametrize("case", VALID_ENTRIES)
def test_valid_entry_insert(case, database_api):
    database_api.add(case)
    entries = database_api.get_all()
    entry = entries[0]

    assert len(entries) == 1

    for field, expected_value in case.items():
        assert entry[field] == expected_value


# Ensures missing required fields trigger validation errors.
@pytest.mark.create
@pytest.mark.parametrize("case", MISSING_FIELD_ENTRIES)
def test_missing_field_insert(case, database_api):
    with pytest.raises(EntryException):
        database_api.add(case)


# Ensures invalid field types are rejected by the API.
@pytest.mark.create
@pytest.mark.parametrize("case", INVALID_FIELD_ENTRIES)
def test_invalid_field_type_insert(case, database_api):
    with pytest.raises(EntryException):
        database_api.add(case)


# Verifies multiple inserts work correctly and all entries are stored.
@pytest.mark.create
@pytest.mark.parametrize("count", INSERT_COUNTS)
def test_multiple_inserts(count, database_api):
    for i in range(count):
        database_api.add(entry_data_generator(i))

    entries = database_api.get_all()

    for entry in entries:
        assert "company" in entry
        assert "job_title" in entry

    assert len(entries) == count


# ---------------------READ---------------------#
# Confirms get_all returns all inserted entries with correct data.
@pytest.mark.read
@pytest.mark.parametrize("count", [0, ENTRY_GENERATOR_COUNT])
def test_get_all_entries(count, database_api):
    expected_entries = {}
    for i in range(count):
        entry = entry_data_generator(i)
        entry_id = database_api.add(entry)
        expected_entries[entry_id] = entry

    entries = database_api.get_all()
    assert len(entries) == count

    for entry in entries:
        expected = expected_entries[entry["id"]]
        for field in expected.keys():
            assert entry[field] == expected[field]


# Ensures retrieval by ID returns the exact matching entry.
@pytest.mark.read
@pytest.mark.parametrize("expected", VALID_ENTRIES)
def test_get_by_valid_id(expected, database_api):
    expected_id = database_api.add(expected)
    entries = database_api.get_by({"id": expected_id})

    assert len(entries) == 1

    entry = entries[0]

    assert entry["id"] == expected_id
    for field, value in expected.items():
        assert entry[field] == value


# Verifies querying a non-existent ID returns an empty result.
@pytest.mark.read
@pytest.mark.parametrize("case", INVALID_ID_GET_BY)
def test_get_by_invalid_id(case, database_api):
    for i in range(case["count"]):
        database_api.add(entry_data_generator(i))

    entries = database_api.get_by(case["filter"])
    assert entries == []


# Tests filtering using a single field condition.
@pytest.mark.read
@pytest.mark.parametrize("case", SINGLE_CONDITION_GET_BY)
def test_get_by_single_condition(case, database_api):
    for i in range(ENTRY_GENERATOR_COUNT):
        database_api.add(entry_data_generator(i))

    entries = database_api.get_by(case["filter"])

    assert len(entries) > 0

    for entry in entries:
        for field, value in case["filter"].items():
            assert entry[field] == value


# Tests filtering with multiple conditions (logical AND behavior).
@pytest.mark.read
@pytest.mark.parametrize("case", MULTIPLE_CONDITION_GET_BY)
def test_get_by_multiple_condition(case, database_api):
    for i in range(ENTRY_GENERATOR_COUNT):
        database_api.add(entry_data_generator(i))

    entries = database_api.get_by(case["filter"])

    assert len(entries) > 0

    for entry in entries:
        for field, value in case["filter"].items():
            assert entry[field] == value


# Ensures valid filters that match no records return an empty list.
@pytest.mark.read
@pytest.mark.parametrize("case", GET_BY_NO_MATCH)
def test_get_by_no_match(case, database_api):
    for i in range(ENTRY_GENERATOR_COUNT):
        database_api.add(entry_data_generator(i))

    entries = database_api.get_by(case["filter"])

    assert len(entries) == 0
    assert entries == []


# Ensures invalid filter fields raise an exception.
@pytest.mark.read
@pytest.mark.parametrize("case", INVALID_FIELD_GET_BY)
def test_get_by_invalid_filter_field(case, database_api):
    for i in range(ENTRY_GENERATOR_COUNT):
        database_api.add(entry_data_generator(i))

    with pytest.raises(EntryException):
        database_api.get_by(case["filter"])


# --------------------UPDATE--------------------#
# Verifies that all fields can be updated successfully.
@pytest.mark.update
@pytest.mark.parametrize("case", FULL_UPDATE)
def test_full_update(case, database_api):
    entry_id = database_api.add(entry_data_generator(1))
    database_api.update(entry_id, case["new_data"])
    entry = database_api.get_by({"id": entry_id})[0]

    for field, expected_value in case["new_data"].items():
        assert entry[field] == expected_value


# Verifies partial updates modify only specified fields.
@pytest.mark.update
@pytest.mark.parametrize("case", PARTIAL_UPDATE)
def test_partial_update(case, database_api):
    entry_id = database_api.add(entry_data_generator(1))
    database_api.update(entry_id, case["new_data"])
    entry = database_api.get_by({"id": entry_id})[0]

    for field, expected_value in case["new_data"].items():
        assert entry[field] == expected_value


# Ensures updating a non-existent ID in an empty DB raises an error.
@pytest.mark.update
def test_update_invalid_id_empty_db(database_api):
    invalid_id = 375092348
    with pytest.raises(EntryException):
        database_api.update(invalid_id, {"company": "Indeed"})


# Ensures updating a non-existent ID when data exists raises an error.
@pytest.mark.update
def test_update_invalid_id_with_existing_data(database_api):
    database_api.add(entry_data_generator(1))
    invalid_id = 9999
    with pytest.raises(EntryException):
        database_api.update(invalid_id, {"company": "Indeed"})


# Ensures invalid update payloads are rejected.
@pytest.mark.update
@pytest.mark.parametrize("case", INVALID_UPDATE_PAYLOADS)
def test_invalid_update_payload(case, database_api):
    entry_id = database_api.add(entry_data_generator(1))
    with pytest.raises(EntryException):
        database_api.update(entry_id, case["new_data"])


# --------------------DELETE--------------------#
# Verifies that deleting a valid ID removes only that entry.
@pytest.mark.delete
@pytest.mark.parametrize("case", DELETE_VALID_ID_CASES)
def test_delete_valid_id(case, database_api):
    added_entries = {}

    for i in range(case["count"]):
        entry_data = entry_data_generator(i)
        entry_id = database_api.add(entry_data)
        added_entries[entry_id] = entry_data

    assert case["id"] in added_entries.keys()

    added_entries.pop(case["id"])
    database_api.delete(case["id"])
    entries = database_api.get_all()

    assert len(entries) == case["count"] - 1

    for entry in entries:
        expected = added_entries[entry["id"]]

        for field, value in expected.items():
            assert entry[field] == value


# Ensures deleting a non-existent ID raises an error.
@pytest.mark.delete
@pytest.mark.parametrize("case", DELETE_INVALID_ID_CASES)
def test_delete_invalid_id(case, database_api):
    entry_ids = []

    for i in range(case["count"]):
        entry_data = entry_data_generator(i)
        entry_ids.append(database_api.add(entry_data))

    assert case["id"] not in entry_ids

    with pytest.raises(EntryException):
        database_api.delete(case["id"])


# Verifies that all entries can be deleted at once.
@pytest.mark.delete
@pytest.mark.parametrize("case", DELETE_ALL_CASES)
def test_delete_all(case, database_api):
    entry_ids = []

    for i in range(case["count"]):
        entry_data = entry_data_generator(i)
        entry_ids.append(database_api.add(entry_data))

    assert len(entry_ids) == case["count"]

    entries = database_api.get_all()
    assert len(entries) == case["count"]

    database_api.delete_all()
    entries = database_api.get_all()
    assert entries == []
