"""SQLAlchemy ORM model for a job application entry."""

from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Entry(Base):
    __tablename__ = "Entry"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(30))
    job_title: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(30), default="Pending start")
    created_at: Mapped[date] = mapped_column(
        Date, default=lambda: datetime.now(timezone.utc).date()
    )
    response_at: Mapped[Optional[date]] = mapped_column(Date, default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "job_title": self.job_title,
            "status": self.status,
            "created_at": self.created_at,
            "response_at": self.response_at,
        }

    def __repr__(self):
        return f"{self.id} {self.company} {self.job_title}"
