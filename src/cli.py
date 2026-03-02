import typer
import sqlalchemy as sa
from tabulate import tabulate
from .db import engine
from .db import SessionLocal
from .db import Base
from .models import Entry

app = typer.Typer()

def init():
    Base.metadata.create_all(bind=engine)
    app()

@app.command()
def add(company: str, job_title:str, application_status:str):
    """
    Inserts a new Job Application entry to the database
    """
    session = SessionLocal()
    try:
        job = Entry(company=company, job_title=job_title, application_status=application_status)
        session.add(job)
        session.commit()
    finally:
        session.close()

@app.command()
def show_all():
    """
    Prints all the Job Application entries in the database
    """
    session = SessionLocal()
    try:
        stmt = sa.select(Entry)
        results = session.execute(stmt).fetchall()
        headers = Entry.__mapper__.columns.keys()
        print(tabulate(results, tablefmt="pretty"))
    finally:
        session.close()

@app.command()
def reset_db():
    """
    TODO: removes all entries and resets id
    """
    pass

if __name__ == "__main__":
    init()