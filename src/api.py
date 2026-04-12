from .models import Entry
from .exceptions import (
    MissingCompany,
    MissingJobTitle,
    MissingUpdateFields,
    MissingSearchCriteria,
    EntryNotFound,
)
from .data_utils import filter_empty_fields
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
    def add(self, entry: Entry) -> None:
        """
        Adds a new Entry to the database.

        Validates required fields before persisting.

        Args:
            entry (Entry): Entry instance to add.
        """
        # Validate required fields before inserting into the database.
        if not entry.company:
            raise MissingCompany()
        if not entry.job_title:
            raise MissingJobTitle()

        self.session.add(entry)

    # Retrieves entries matching given filters. Filters are cleaned before querying.
    def get_by(self, fields: dict) -> list[dict]:
        """
        Retrieves entries matching provided filters.

        Args:
            fields (dict): Filter criteria.

        Returns:
            list[dict]: Matching entries.
        """
        # Remove empty or invalid fields from the input.
        fields = filter_empty_fields(fields)

        # Ensure at least one valid filter is provided.
        if not fields:
            raise MissingSearchCriteria()

        return [
            entry.to_dict()
            for entry in self.session.query(Entry).filter_by(**fields).all()
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
        # Clean input data by removing empty fields.
        data = filter_empty_fields(data)
        # Retrieve the entry to ensure it exists before updating.
        entry = self.session.query(Entry).filter(Entry.id == id).first()

        # Prevent updates with no valid fields.
        if not data:
            raise MissingUpdateFields()
        # Raise error if the entry does not exist.
        if not entry:
            raise EntryNotFound(id)

        entry.update(data)

    # Deletes an entry by id after verifying its existence.
    def delete(self, id: int) -> None:
        """
        Deletes an entry by id.

        Args:
            id (int): Entry identifier.
        """
        # Retrieve the entry to confirm it exists.
        entry = self.session.query(Entry).filter(Entry.id == id).first()

        # Raise error if the entry does not exist.
        if not entry:
            raise EntryNotFound(id)

        self.session.delete(entry)

    # Deletes all entries in the table (bulk operation).
    def delete_all(self) -> None:
        """
        Deletes all entries from the database.
        """
        self.session.query(Entry).delete()
