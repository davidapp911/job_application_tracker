import typer
import sqlalchemy as sa
from sqlalchemy import text
from tabulate import tabulate
from .db import engine
from .db import SessionLocal
from .db import Base
from .models import Entry

app = typer.Typer()

@app.command()
def add(company: str, job_title:str):
    """
    Inserts a new Job Application entry to the database
    """
    session = SessionLocal()
    try:
        job = Entry(company=company, job_title=job_title)
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
    Removes all entries and resets id
    """
    try:
        session = SessionLocal()
        session.execute(Entry.__table__.delete())
        session.execute(
            text(f"DELETE FROM sqlite_sequence WHERE name='{Entry.__tablename__}'")
        )
        session.commit()
    finally:
        session.close()
        
@app.command()
def search_entry(id: int):
    """
    TODO: return entry that has input id
    """
    pass


if __name__ == "__main__":
    app()