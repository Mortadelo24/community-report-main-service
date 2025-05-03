from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .report import Report


class ComplaintBase(SQLModel):
    pass


class Complaint(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    reports: list["Report"] = Relationship(back_populates="complaint")
    text: str

