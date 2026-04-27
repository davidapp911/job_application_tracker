"""API layer for managing job application entries."""

from typing import Optional

from sqlalchemy.orm import Session

from .data_utils import filter_empty_fields
from .exceptions import (
    EmptyField,
    EntryNotFound,
    FieldNotAllowed,
    MissingSearchCriteria,
    MissingUpdateFields,
    WrongFieldType,
)
from .models import Entry


class EntryDB:
    """Data access layer for Entry objects."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, data: dict) -> int:
        """Validate data, persist a new Entry, and return its id."""
        validated_data = _validate_entry_data(data)
        entry = Entry(**validated_data)
        self.session.add(entry)
        # Flush so the DB assigns an id before returning.
        self.session.flush()
        return entry.id

    def get_by(self, fields: dict) -> list[dict]:
        """Return entries matching the provided filter dict."""
        filtered = filter_empty_fields(fields)
        search_filter = _validate_filter_data(filtered)
        # Require at least one filter to avoid a full table scan.
        if not search_filter:
            raise MissingSearchCriteria()
        return [entry.to_dict() for entry in self.session.query(Entry).filter_by(**search_filter).all()]

    def get_all(self) -> list[dict]:
        """Return all entries."""
        return [entry.to_dict() for entry in self.session.query(Entry).all()]

    def update(self, id: int, data: dict) -> None:
        """Update fields of an existing entry by id."""
        filtered_data = filter_empty_fields(data, include_empty_str=False)
        entry = self.session.query(Entry).filter(Entry.id == id).first()
        if not filtered_data:
            raise MissingUpdateFields()
        if not entry:
            raise EntryNotFound(id)
        validated_data = _validate_entry_data(filtered_data, partial=True)
        # SQLAlchemy tracks attribute changes; commit is handled by the session context.
        for k, v in validated_data.items():
            setattr(entry, k, v)

    def delete(self, id: int) -> None:
        """Delete an entry by id."""
        entry = self.session.query(Entry).filter(Entry.id == id).first()
        if not entry:
            raise EntryNotFound(id)
        self.session.delete(entry)

    def delete_all(self) -> None:
        """Delete all entries."""
        self.session.query(Entry).delete()


def _validate_entry_data(data: dict, partial: Optional[bool] = False) -> dict:
    REQUIRED_FIELDS = ["company", "job_title"]
    ALLOWED_FIELDS = ["company", "job_title", "status"]

    if not partial:
        for field in REQUIRED_FIELDS:
            value = data.get(field)
            if value is None or not isinstance(value, str) or value.strip() == "":
                raise EmptyField(field)

    for field, value in data.items():
        if field not in ALLOWED_FIELDS:
            raise FieldNotAllowed(field)
        if not isinstance(value, str):
            raise WrongFieldType("str", type(value))
        if field == "status":
            # Status is optional on creation but must be non-empty when updated.
            if not partial:
                if value.strip() == "":
                    continue
            else:
                if value.strip() == "":
                    raise EmptyField(field)
        else:
            if value.strip() == "":
                raise EmptyField(field)

    return data


def _validate_filter_data(data: dict) -> dict:
    ALLOWED_FIELDS = ["id", "company", "job_title", "status"]

    for field, value in data.items():
        if field == "id":
            # id is matched by integer equality, not string comparison.
            if isinstance(value, int):
                continue
            else:
                raise WrongFieldType("int", type(value))
        else:
            if field not in ALLOWED_FIELDS:
                raise FieldNotAllowed(field)
            if isinstance(value, str):
                continue
            else:
                raise WrongFieldType("str", type(value))

    return data
