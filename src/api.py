from .models import Entry
from .exceptions import (
    MissingCompany,
    MissingJobTitle,
    MissingUpdateFields,
    MissingSearchCriteria,
    EntryNotFound,
)
from .data_utils import filter_empty_fields


class EntryDB:
    def __init__(self, session):
        self.session = session

    def add(self, entry: Entry):
        if not entry.company:
            raise MissingCompany()
        if not entry.job_title:
            raise MissingJobTitle()

        self.session.add(entry)

    def get_by(self, fields):
        fields = filter_empty_fields(fields)

        if not fields:
            raise MissingSearchCriteria()

        return [
            entry.to_dict()
            for entry in self.session.query(Entry).filter_by(**fields).all()
        ]

    def get_all(self):
        return [entry.to_dict() for entry in self.session.query(Entry).all()]

    def update(self, id, data):
        data = filter_empty_fields(data)
        entry = self.session.query(Entry).filter(Entry.id == id)

        if not data:
            raise MissingUpdateFields()
        if not entry:
            raise EntryNotFound(id)

        entry.update(data)

    def delete(self, id):
        entry = self.session.query(Entry).filter(Entry.id == id).first()

        if not entry:
            raise EntryNotFound(id)

        self.session.delete(entry)
