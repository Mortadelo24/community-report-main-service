from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from .links import UserCommunityLink
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .community import Community

class UserBase(SQLModel):
    display_name: str | None = None
    email: EmailStr

class UserFirebase(UserBase):
    id: str 


class UserPublic(UserBase):
    id: int


class UserToken(UserPublic):
    pass

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    firebase_id: str | None = Field(default=None, index=True, unique=True)
    communities_joined: list["Community"] = Relationship(back_populates="members", link_model=UserCommunityLink)
    owned_communities: list["Community"] = Relationship(back_populates="owner")