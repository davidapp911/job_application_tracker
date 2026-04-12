"""
Database models for the job application tracker.

Defines ORM mappings using SQLAlchemy for persisting and retrieving
job application data.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .db import Base


# ORM model representing a job application entry.
class Entry(Base):
    __tablename__ = "Entry"

    id: Mapped[int] = mapped_column(primary_key=True)  # primary key identifier
    company: Mapped[str] = mapped_column(String(30))  # company name (limited length)
    job_title: Mapped[str] = mapped_column(String(30))  # job title (limited length)
    application_status: Mapped[str] = mapped_column(
        (String(30)), default="Pending start"
    )  # current status of the application with a default value

    # Converts the Entry instance into a dictionary for serialization or display.
    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "job_title": self.job_title,
            "application_status": self.application_status,
        }

    # Provides a string representation of the Entry instance (useful for debugging).
    def __repr__(self):
        print(f"{self.id} {self.company} {self.job_title}")
