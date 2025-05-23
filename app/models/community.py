from sqlmodel import SQLModel, Field, Relationship
from .links import UserCommunityLink
from .user import User
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .report import Report
    from .invitation import Invitation


class CommunityBase(SQLModel):
    name: str = Field(min_length=4, max_length=30)


class CommunityCreate(CommunityBase):
    pass


class CommunityPublic(CommunityBase):
    id: UUID
    owner_id: UUID


class Community(CommunityBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    members: list["User"] = Relationship(back_populates="communities_joined", link_model=UserCommunityLink)
    owner_id: UUID = Field(foreign_key="user.id")
    owner: User | None = Relationship(back_populates="owned_communities")
    reports: list["Report"] = Relationship(back_populates="community")
    invitations: list["Invitation"] = Relationship(back_populates="community")

