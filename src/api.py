import pathlib
from .db import Base
from .db import engine
from .models import Entry

#TODO: Implement the functions
__all__ = [
    "EntryDB"
    "EntryException",
    "MissingCompany",
    "MissingPosition"
]

class EntryException(Exception):
    pass

class MissingCompany(Exception):
    pass

class MissingJobTitle(Exception):
    pass


class EntryDB:
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def add_entry(self, entry: Entry):
        if not entry.company:
            raise MissingCompany
        if not entry.job_title:
            raise MissingJobTitle

    def get_entry(self):
        pass

    def update_entry(self):
        pass

    def delete_entry(self):
        pass

    def get_entries(self):
        pass

    def update_entry_status(self):
        pass


def main():
    db = EntryDB()
    print(f"Hello {2}")

if __name__ == "__main__":
    main()