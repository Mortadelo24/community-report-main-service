from sqlmodel import SQLModel, Relationship, Field
from .user import User
from .community import Community
from uuid import UUID, uuid4


class ReportBase(SQLModel):
    complaint: str = Field(min_length=8)

class ReportCreate(ReportBase):
    community_id: UUID

class ReportPublic(ReportBase):
    id: UUID

class Report(ReportBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user: User = Relationship(back_populates="reports")
    community: Community = Relationship(back_populates="reports")
    user_id: UUID = Field(foreign_key="user.id")
    community_id: UUID = Field(foreign_key="community.id")
