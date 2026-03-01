import sqlalchemy as sa
from tabulate import tabulate
from .db import engine
from .db import SessionLocal
from .db import Base
from .models import Entry


def init():
    Base.metadata.create_all(bind=engine)

def add(company, job_title, application_status):
    session = SessionLocal()
    try:
        job = Entry(company=company, job_title=job_title, application_status=application_status)
        session.add(job)
        session.commit()
    finally:
        session.close()

def show_all():
    session = SessionLocal()
    try:
        stmt = sa.select(Entry)
        results = session.execute(stmt).fetchall()
        headers = Entry.__mapper__.columns.keys()
        print(tabulate(results, tablefmt="pretty"))
    finally:
        session.close()

def main():
    pass


if __name__ == "__main__":
    init()

    # Temporary manual testing
    add("Google", "Software Engineer", "accepted")
    add("Meta", "Backend Engineer", "rejected")

    print("\nAll Jobs:")
    show_all()