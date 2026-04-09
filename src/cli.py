import typer
from typing import Optional
from tabulate import tabulate
from contextlib import contextmanager
from .db import SessionLocal
from .models import Entry
from .api import EntryDB
from .exceptions import EntryException

app = typer.Typer()


@app.command()
def new_entry(company: str = typer.Option(...), job_title: str = typer.Option(...)):
    """
    Inserts a new Job Application entry to the database
    """
    try:
        with database_session() as db:
            db.add(Entry(company=company, job_title=job_title))
    except EntryException as e:
        typer.secho(f"{e.__class__.__name__}: {e.message}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def show_all():
    """
    Prints all the Job Application entries in the database
    """
    with database_session() as db:
        entries = db.get_all()
        print_table(entries)


@app.command()
def search_by(
    id: str,
    company: Optional[str] = None,
    job_title: Optional[str] = None,
    application_status: Optional[str] = None,
):
    """
    Return job entry that has id that matches the input id
    """
    query_filter = {
        "id": id,
        "company": company,
        "job_title": job_title,
        "application_status": application_status,
    }

    query_filter = {k: v for k, v in query_filter.items() if v is not None}

    with database_session() as db:
        entries = db.get_by(query_filter)
        print_table(entries)


@app.command()
def update_entry(
    id: Optional[str] = None,
    company: Optional[str] = None,
    job_title: Optional[str] = None,
):
    """
    Updates company and/or job_title of an entry with a given id
    """
    update_data = {
        "company": company,
        "job_title": job_title,
    }

    update_data = {k: v for k, v in update_data.items() if v is not None}

    with database_session() as db:
        db.update(id, update_data)


@app.command()
def update_status(id: str, status: str):
    """
    Updates the Job application entry status
    """
    with database_session() as db:
        db.update(id, {"application_status": status})


@app.command()
def delete_entry(id: str):
    """
    Removes the entry that has the id value given by the user
    """
    with database_session() as db:
        db.delete(id)


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


def print_table(entries):
    if not entries:
        print("No entries found")
    else:
        print(f"\n{tabulate(entries, headers='keys')}\n")


if __name__ == "__main__":
    app()
