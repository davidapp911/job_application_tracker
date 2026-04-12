"""
CLI utility helpers.

Includes database session management and output formatting utilities
used by the command-line interface.
"""

from typing import Iterator
import typer
from tabulate import tabulate
from contextlib import contextmanager
from .db import SessionLocal
from .api import EntryDB


# Context manager that provides a database session wrapped in EntryDB.
# Handles commit on success, rollback on error, and ensures the session is closed.
@contextmanager
def database_session() -> Iterator[EntryDB]:
    """
    Provides a transactional database session wrapped in EntryDB.

    Yields:
        EntryDB: API layer interface for database operations.

    Ensures:
        - Commit on success
        - Rollback on failure
        - Session is always closed
    """
    # Create a new SQLAlchemy session.
    session = SessionLocal()
    # Wrap the session with the API layer.
    db = EntryDB(session)

    try:
        # Provide the database interface to the caller.
        yield db
        # Commit the transaction if no exceptions occurred.
        session.commit()
    except:
        # Roll back the transaction if an exception occurs.
        session.rollback()
        raise
    finally:
        # Always close the session to release resources.
        session.close()


# Prints a list of dictionary entries in a formatted table.
# Displays a message if no entries are provided.
def print_table(entries: list[dict]) -> None:
    """
    Displays a list of dictionaries as a formatted table.

    Args:
        entries (list[dict]): Data to display.
    """
    if not entries:
        print("No entries found")
    else:
        print(f"\n{tabulate(entries, headers='keys')}\n")


# Handles CLI errors by printing a formatted message and exiting the program.
def handle_cli_error(e) -> None:
    """
    Handles CLI-level exceptions by printing a formatted error and exiting.

    Args:
        e: Exception instance to handle.
    """
    typer.secho(f"{e.__class__.__name__}: {e.message}", fg=typer.colors.RED)
    raise typer.Exit(code=1)


# Prints a success message in green for CLI feedback.
def success(message):
    """
    Prints a success message in green.

    Args:
        message (str): Message to display.
    """
    typer.secho(message, fg=typer.colors.GREEN)
