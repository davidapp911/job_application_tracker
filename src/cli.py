import typer
from tabulate import tabulate
from contextlib import contextmanager
from .db import SessionLocal
from .models import Entry
from .api import EntryDB

app = typer.Typer()

@app.command()
def new_entry(
    company: str, 
    job_title:str
    ):
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
def search_by(
    id: str = None, 
    company: str = None, 
    job_title: str = None, 
    application_status:str = None
    ):
    """
    Return job entry that has id that matches the input id
    """
    query_filter = {
        "id": id,
        "company": company,
        "job_title": job_title,
        "application_status": application_status
    }

    query_filter = {k: v for k, v in query_filter.items() if v is not None}

    with database_session() as db:
        entries = db.get_by(query_filter)
        print(tabulate(entries, headers="keys"))

@app.command()
def delete_entry(id: str = None):
    """
    TODO: removes the entry that has the id value given by the user
    """
    pass

@app.command()
def reset_db():
    """
    TODO: removes all entries and resets id
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