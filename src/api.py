"""
API layer for interacting with Entry objects.

This module defines the EntryDB class, which acts as the data access layer
between the application and the database. It encapsulates CRUD operations
and enforces business rules such as:

- Validating required fields before inserting or updating entries
- Cleaning and normalizing input data via filter_empty_fields
- Ensuring existence of records before update/delete operations
- Raising domain-specific exceptions for invalid operations

This separation keeps database logic centralized and decoupled from
the CLI or other interfaces.
"""

from typing import Optional

from .models import Entry
from .data_utils import filter_empty_fields
from .exceptions import (
    EmptyField,
    WrongFieldType,
    FieldNotAllowed,
    MissingUpdateFields,
    MissingSearchCriteria,
    EntryNotFound,
)
from sqlalchemy.orm import Session


class EntryDB:
    """
    Data access layer for Entry objects.

    Encapsulates all CRUD operations and enforces business rules
    before interacting with the database.
    """

    # Initializes the EntryDB with a SQLAlchemy session instance.
    def __init__(self, session: Session) -> None:
        """
        Initializes the EntryDB with a SQLAlchemy session.

        Args:
            session (Session): Active database session.
        """
        self.session = session

    # Adds a new Entry to the session after validating required fields.
    def add(self, data: dict) -> int:
        """
        Adds a new Entry to the database.

        Validates required fields before persisting.

        Args:
            entry (Entry): Entry instance to add.
        """
        # Validate and normalize input before model creation.
        validated_data = _validate_entry_data(data)

        # Create ORM object only after data is guaranteed valid.
        entry = Entry(**validated_data)

        # Add to session and flush so the database assigns an ID immediately.
        self.session.add(entry)
        self.session.flush()

        return entry.id

    # Retrieves entries matching given filters. Filters are cleaned before querying.
    def get_by(self, fields: dict) -> list[dict]:
        """
        Retrieves entries matching provided filters.

        Args:
            fields (dict): Filter criteria.

        Returns:
            list[dict]: Matching entries.
        """
        # Validate and sanitize filter input (no invalid types or fields).
        filtered = filter_empty_fields(fields)
        search_filter = _validate_filter_data(filtered)

        # Require at least one filter to avoid full table scans.
        if not search_filter:
            raise MissingSearchCriteria()

        return [
            entry.to_dict()
            for entry in self.session.query(Entry).filter_by(**search_filter).all()
        ]

    # Retrieves all entries from the database.
    def get_all(self) -> list[dict]:
        """
        Retrieves all entries from the database.

        Returns:
            list[dict]: All entries.
        """
        return [entry.to_dict() for entry in self.session.query(Entry).all()]

    # Updates an existing entry by id using provided data.
    def update(self, id: int, data: dict) -> None:
        """
        Updates an existing entry by id.

        Args:
            id (int): Entry identifier.
            data (dict): Fields to update.
        """
        filtered_data = filter_empty_fields(data, include_empty_str=False)

        # Retrieve the entry to ensure it exists before updating.
        entry = self.session.query(Entry).filter(Entry.id == id).first()

        # Prevent updates with no provided data.
        if not filtered_data:
            raise MissingUpdateFields()

        # Ensure the target entry exists before applying changes.
        if not entry:
            raise EntryNotFound(id)

        # Validate only provided fields (partial update allowed).
        validated_data = _validate_entry_data(filtered_data, partial=True)

        # Apply updates dynamically; SQLAlchemy tracks these changes automatically.
        for k, v in validated_data.items():
            setattr(entry, k, v)

    # Deletes an entry by id after verifying its existence.
    def delete(self, id: int) -> None:
        """
        Deletes an entry by id.

        Args:
            id (int): Entry identifier.
        """
        # Retrieve entry to ensure it exists before deletion.
        entry = self.session.query(Entry).filter(Entry.id == id).first()

        # Prevent deleting non-existent records.
        if not entry:
            raise EntryNotFound(id)

        # Mark object for deletion; commit handled externally.
        self.session.delete(entry)

    # Deletes all entries in the table (bulk operation).
    def delete_all(self) -> None:
        """
        Deletes all entries from the database.
        """
        self.session.query(Entry).delete()


def _validate_entry_data(data: dict, partial: Optional[bool] = False) -> dict:
    # Fields required for full object creation.
    REQUIRED_FIELDS = ["company", "job_title"]
    # Fields allowed to be passed into the API.
    ALLOWED_FIELDS = ["company", "job_title", "status"]

    # Full validation: enforce required fields only when not performing partial updates.
    if not partial:
        for field in REQUIRED_FIELDS:
            value = data.get(field)
            if value is None or not isinstance(value, str) or value.strip() == "":
                raise EmptyField(field)

    # Validate each provided field individually.
    for field, value in data.items():

        # Reject unknown fields early.
        if field not in ALLOWED_FIELDS:
            raise FieldNotAllowed(field)

        # Enforce string type for all fields.
        if not isinstance(value, str):
            raise WrongFieldType("str", type(value))

        # Field-specific validation rules.
        if field == "status":
            # Status is optional on creation but cannot be empty on update.
            if not partial:
                if value.strip() == "":
                    continue
            else:
                if value.strip() == "":
                    raise EmptyField(field)
        else:
            # Required fields must not be empty strings.
            if value.strip() == "":
                raise EmptyField(field)

    return data


def _validate_filter_data(data: dict) -> dict:
    ALLOWED_FIELDS = ["id", "company", "job_title", "status"]

    # Validate filter fields and enforce allowed types.
    for field, value in data.items():
        # ID must be an integer for exact matching.
        if field == "id":
            if isinstance(value, int):
                continue
            else:
                raise WrongFieldType("int", type(value))
        else:
            # Validate string-based filters.
            if field not in ALLOWED_FIELDS:
                raise FieldNotAllowed(field)
            if isinstance(value, str):
                continue
            else:
                raise WrongFieldType("str", type(value))

    return data
