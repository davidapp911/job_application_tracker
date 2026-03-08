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
    application_status: Mapped[str] = mapped_column((String(30)), default="Pending start")

    def __repr__(self) -> str:
        return f"Job(id={self.id!r}, company={self.company!r}, job_title={self.job_title!r}, application_status={self.application_status!r})"