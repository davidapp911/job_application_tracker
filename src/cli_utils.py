"""Database session management and CLI output helpers."""

from contextlib import contextmanager
from typing import Iterator

import typer
from tabulate import tabulate

from .api import EntryDB
from .db import SessionLocal


@contextmanager
def database_session() -> Iterator[EntryDB]:
    """Provide a transactional EntryDB session.

    Commits on success, rolls back on exception, always closes the session.
    """
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


def print_table(entries: list[dict]) -> None:
    """Print entries as a formatted table, or a message if the list is empty."""
    if not entries:
        print("No entries found.")
    else:
        print(f"\n{tabulate(entries, headers='keys')}\n")


def handle_cli_error(e) -> None:
    """Print the exception message in red and exit with code 1."""
    typer.secho(f"{e.__class__.__name__}: {e.message}", fg=typer.colors.RED)
    raise typer.Exit(code=1)


def success(message):
    """Print a success message in green."""
    typer.secho(message, fg=typer.colors.GREEN)
