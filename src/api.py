from .models import Entry

#TODO: Implement the functions
__all__ = [
    "EntryDB",
    "EntryException",
    "MissingCompany",
    "MissingJobTitle"
]

class EntryException(Exception):
    pass

class MissingCompany(Exception):
    pass

class MissingJobTitle(Exception):
    pass

class EntryDB:
    def __init__(self, session):
        self.session = session

    def add(self, entry: Entry):
        if not entry.company:
            raise MissingCompany
        if not entry.job_title:
            raise MissingJobTitle
        
        self.session.add(entry)

    def get_by(self, fields):
        return [entry.to_dict() for entry in self.session.query(Entry).filter_by(**fields).all()]
        
    def get_all(self):
        return [entry.to_dict() for entry in self.session.query(Entry).all()]
    
    def update(self, id, new_data):
        self.session.query(Entry).filter(Entry.id == id).update(new_data)

    def delete(self, id):
        entry = self.session.query(Entry).filter(Entry.id == id).first()
        if entry:
            self.session.delete(entry)

