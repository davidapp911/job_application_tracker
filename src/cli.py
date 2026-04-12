"""
Command-line interface for the job application tracker.

Defines commands for creating, retrieving, updating, and deleting
job application entries.
"""

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
) -> None:
    """
    Creates a new job application entry.

    Accepts company and job_title as positional arguments,
    constructs an Entry object, and persists it using the API layer.
    """
    try:
        with database_session() as db:
            db.add(Entry(company=company, job_title=job_title))
    except EntryException as e:
        handle_cli_error(e)

    success("Entry created successfully.")


@app.command()
def list() -> None:
    """
    Retrieves and displays all job application entries.

    Uses the API layer to fetch all records and prints them in a table format.
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
) -> None:
    """
    Searches for entries using one or more optional filters.

    Any combination of id, company, job_title, or application_status
    can be provided. Only non-empty values are used in the query.
    """
    # Build a filter dictionary from CLI inputs (may include None values).
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
    id: int = typer.Argument(...),
    company: Optional[str] = typer.Option(None),
    job_title: Optional[str] = typer.Option(None),
) -> None:
    """
    Updates an existing job application entry.

    Requires an id (positional argument) and accepts optional fields
    to update. Only provided (non-empty) fields will be modified.
    """
    # Collect fields to update; None values will be filtered out later.
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
def delete(id: int = typer.Argument(...)) -> None:
    """
    Deletes a job application entry by id.
    """
    try:
        with database_session() as db:
            db.delete(id)
    except EntryException as e:
        handle_cli_error(e)

    success("Job entry deleted successfully.")


@app.command()
def reset() -> None:
    """
    Deletes all job application entries after user confirmation.

    Prompts the user before performing a destructive bulk operation.
    """
    # Prompt user for confirmation before destructive operation.
    flag = input(
        "This will remove all the entries in the database. Are you sure? [y/n]"
    )

    # Only proceed if user explicitly confirms with 'y'.
    if flag == "y":
        # Execute bulk delete through the API layer.
        try:
            with database_session() as db:
                db.delete_all()
        except EntryException as e:
            handle_cli_error(e)

        success("All entries were deleted successfully.")


# Entry point for running the CLI application directly.
if __name__ == "__main__":
    app()
