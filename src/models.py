from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .db import Base


class Entry(Base):
    __tablename__ = "Entry"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(30))
    job_title: Mapped[str] = mapped_column(String(30))
    application_status: Mapped[str] = mapped_column((String(30)))

    def __repr__(self) -> str:
        return f"Job(id={self.id!r}, company={self.company!r}, job_title={self.job_title!r}, application_status={self.application_status!r})"
    
def main():
    job_data ={
        "id": 1,
        "company": "apple",
        "job_title": "software nerd",
        "application_status": "Accepted"
    }
    
    job1 = Entry(**job_data)
    print(job1)

    job2 = Entry(id=2, company="dell", job_title="qa engineer", application_status="Rejected")
    print(job2)

if __name__ == "__main__":
    main()