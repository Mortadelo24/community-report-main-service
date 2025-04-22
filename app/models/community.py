from sqlmodel import SQLModel, Field, Relationship
from .links import UserCommunityLink
from .user import User

class CommunityBase(SQLModel):
    name: str

class CommunityCreate(CommunityBase):
    pass

class CommunityPublic(CommunityBase):
    id: int

class Community(CommunityBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    members: list["User"] = Relationship(back_populates="communities_joined", link_model=UserCommunityLink)
    
    owner_id: int  = Field(foreign_key="user.id")
    owner: User| None = Relationship(back_populates="owned_communities")