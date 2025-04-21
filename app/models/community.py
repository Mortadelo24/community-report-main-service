from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from .links import UserCommunityLink


if TYPE_CHECKING:
    from .user import User

class CommunityBase(SQLModel):
    name: str

class CommunityCreate(CommunityBase):
    pass

class CommunityPublic(CommunityBase):
    id: int

class Community(CommunityBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    members: list["User"] = Relationship(back_populates="communities", link_model=UserCommunityLink)