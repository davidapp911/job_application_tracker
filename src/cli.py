import typer
from typing import Optional
from .models import Entry
from .exceptions import EntryException
from .cli_utils import database_session, handle_cli_error, success, print_table

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
        handle_cli_error(e)

    success("Entry created succesfully.")


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
    id: Optional[str] = None,
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

    try:
        with database_session() as db:
            entries = db.get_by(query_filter)
    except EntryException as e:
        handle_cli_error(e)

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

    try:
        with database_session() as db:
            db.update(id, update_data)
    except EntryException as e:
        handle_cli_error(e)

    success("Job entry updated successfully.")


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
    try:
        with database_session() as db:
            db.delete(id)
    except EntryException as e:
        handle_cli_error(e)

    success("Job entry deleted succesfully.")


@app.command()
def reset_db():
    """
    TODO: removes all entries and resets id
    """
    pass


if __name__ == "__main__":
    app()
