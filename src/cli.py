import typer
from typing import Optional
from .models import Entry
from .exceptions import EntryException
from .cli_utils import database_session, handle_cli_error, success, print_table

app = typer.Typer()


@app.command()
def add(
    company: str = typer.Argument(...),
    job_title: str = typer.Argument(...),
):
    """
    Inserts a new Job Application entry to the database
    """
    try:
        with database_session() as db:
            db.add(Entry(company=company, job_title=job_title))
    except EntryException as e:
        handle_cli_error(e)

    success("Entry created succesfully.")


@app.command()
def list():
    """
    Prints all the Job Application entries in the database
    """
    with database_session() as db:
        entries = db.get_all()

    print_table(entries)


@app.command()
def search_by(
    id: Optional[str] = typer.Option(None),
    company: Optional[str] = typer.Option(None),
    job_title: Optional[str] = typer.Option(None),
    application_status: Optional[str] = typer.Option(None),
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

    try:
        with database_session() as db:
            entries = db.get_by(query_filter)
    except EntryException as e:
        handle_cli_error(e)

    print_table(entries)


@app.command()
def update(
    id: str = typer.Argument(...),
    company: Optional[str] = typer.Option(None),
    job_title: Optional[str] = typer.Option(None),
):
    """
    Updates company and/or job_title of an entry with a given id
    """
    update_data = {
        "company": company,
        "job_title": job_title,
    }

    try:
        with database_session() as db:
            db.update(id, update_data)
    except EntryException as e:
        handle_cli_error(e)

    success("Job entry updated successfully.")


@app.command()
def delete(id: str = typer.Argument(...)):
    """
    Removes the entry that has the id value given by the user
    """
    try:
        with database_session() as db:
            db.delete(id)
    except EntryException as e:
        handle_cli_error(e)

    success("Job entry deleted successfully.")


@app.command()
def reset():
    """
    TODO: removes all entries and resets id
    """
    pass


if __name__ == "__main__":
    app()
