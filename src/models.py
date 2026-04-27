"""SQLAlchemy ORM model for a job application entry."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Entry(Base):
    __tablename__ = "Entry"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(30))
    job_title: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(30), default="Pending start")

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "job_title": self.job_title,
            "status": self.status,
        }

    def __repr__(self):
        return f"{self.id} {self.company} {self.job_title}"
