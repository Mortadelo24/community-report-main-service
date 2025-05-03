from sqlmodel import SQLModel, Relationship, Field
from .user import User
from .community import Community
from .complaint import Complaint
from uuid import UUID, uuid4
from datetime import datetime


class ReportBase(SQLModel):
    pass


class ReportCreate(ReportBase):
    community_id: UUID
    complaint_id: UUID


class ReportPublic(ReportBase):
    id: UUID
    complaint_id: UUID
    created_at: datetime


class Report(ReportBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    user: User = Relationship(back_populates="reports")
    complaint: Complaint = Relationship(back_populates="reports")
    community: Community = Relationship(back_populates="reports")

    user_id: UUID = Field(foreign_key="user.id")
    complaint_id: UUID = Field(foreign_key="complaint.id")
    community_id: UUID = Field(foreign_key="community.id")
