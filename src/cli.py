import typer
from tabulate import tabulate
from contextlib import contextmanager
from .db import SessionLocal
from .models import Entry
from .api import EntryDB

app = typer.Typer()

@app.command()
def new_entry(company: str, job_title:str):
    """
    Inserts a new Job Application entry to the database
    """
    with database_session() as db:
        db.add(Entry(company=company, job_title=job_title))
        

@app.command()
def show_all():
    """
    Prints all the Job Application entries in the database
    """
    with database_session() as db:
        entries = db.get_all()
        print(tabulate(entries, headers="keys"))

@app.command()
def reset_db():
    """
    TODO: removes all entries and resets id
    """
    pass
        
@app.command()
def search_entry(id: int):
    """
    TODO: return entry that has input id
    """
    pass

@contextmanager
def database_session():
    session = SessionLocal()
    db = EntryDB(session)
    
    try:
        yield db
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    app()