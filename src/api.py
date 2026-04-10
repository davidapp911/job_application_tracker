from .models import Entry
from .exceptions import (
    MissingCompany,
    MissingJobTitle,
    MissingUpdateFields,
    MissingSearchCriteria,
    EntryNotFound,
)


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
        filter = {k: v for k, v in fields.items() if v is not None and v.strip() != ""}

        if not filter:
            raise MissingSearchCriteria()

        return [
            entry.to_dict()
            for entry in self.session.query(Entry).filter_by(**filter).all()
        ]

    def get_all(self):
        return [entry.to_dict() for entry in self.session.query(Entry).all()]

    def update(self, id, new_data):
        new_data = {
            k: v for k, v in new_data.items() if v is not None and v.strip() != ""
        }
        entry = self.session.query(Entry).filter(Entry.id == id)

        if not new_data:
            raise MissingUpdateFields()
        if not entry:
            raise EntryNotFound(id)

        entry.update(new_data)

    def delete(self, id):
        entry = self.session.query(Entry).filter(Entry.id == id).first()

        if not entry:
            raise EntryNotFound(id)

        self.session.delete(entry)
