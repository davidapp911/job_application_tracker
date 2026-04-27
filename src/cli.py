"""CLI commands for creating, retrieving, updating, and deleting job application entries."""

from typing import Optional

import typer

from .cli_utils import (
    database_session,
    handle_cli_error,
    print_table,
    success,
)
from .db import init_db
from .exceptions import EntryException, WrongInputException

init_db()

app = typer.Typer()


@app.command()
def add(
    company: str = typer.Argument(...),
    job_title: str = typer.Argument(...),
) -> None:
    """Add a new job application entry."""
    try:
        with database_session() as db:
            db.add({"company": company, "job_title": job_title})
    except EntryException as e:
        handle_cli_error(e)

    success("Entry created successfully.")


@app.command()
def list() -> None:
    """List all job application entries."""
    with database_session() as db:
        entries = db.get_all()

    print_table(entries)


@app.command()
def search_by(
    id: Optional[int] = typer.Option(None),
    company: Optional[str] = typer.Option(None),
    job_title: Optional[str] = typer.Option(None, "--job_title"),
    status: Optional[str] = typer.Option(None),
) -> None:
    """Search entries by any combination of id, company, job_title, or status."""
    query_filter = {
        "id": id,
        "company": company,
        "job_title": job_title,
        "status": status,
    }

    try:
        with database_session() as db:
            entries = db.get_by(query_filter)
    except EntryException as e:
        handle_cli_error(e)

    print_table(entries)


@app.command()
def update(
    id: int = typer.Argument(...),
    company: Optional[str] = typer.Option(None),
    job_title: Optional[str] = typer.Option(None, "--job_title"),
    status: Optional[str] = typer.Option(None),
) -> None:
    """Update fields of an existing entry by id."""
    update_data = {
        "company": company,
        "job_title": job_title,
        "status": status,
    }

    try:
        with database_session() as db:
            db.update(id, update_data)
    except EntryException as e:
        handle_cli_error(e)

    success("Job entry updated successfully.")


@app.command()
def delete(id: int = typer.Argument(...)) -> None:
    """Delete a job application entry by id."""
    try:
        with database_session() as db:
            db.delete(id)
    except EntryException as e:
        handle_cli_error(e)

    success("Job entry deleted successfully.")


@app.command()
def reset() -> None:
    """Delete all entries after user confirmation."""
    flag = input("This will remove all the entries in the database. Are you sure? [y/n]")

    if flag == "y" or flag == "Y":
        try:
            with database_session() as db:
                db.delete_all()
        except EntryException as e:
            handle_cli_error(e)

        success("All entries were deleted successfully.")
    elif flag == "n" or flag == "N":
        print("Database reset aborted.")
    else:
        handle_cli_error(WrongInputException("Invalid input provided."))


if __name__ == "__main__":
    app()
