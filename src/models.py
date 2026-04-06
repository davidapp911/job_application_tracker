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

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "job_title": self.job_title,
            "application_status": self.application_status
        }
    
    def __repr__(self):
        print(f"{self.id} {self.company} {self.job_title}")