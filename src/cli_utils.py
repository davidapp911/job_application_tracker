import typer
from tabulate import tabulate
from contextlib import contextmanager
from .db import SessionLocal
from .api import EntryDB


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


def handle_cli_error(e):
    typer.secho(f"{e.__class__.__name__}: {e.message}", fg=typer.colors.RED)
    raise typer.Exit(code=1)


def success(message):
    typer.secho(message, fg=typer.colors.GREEN)
