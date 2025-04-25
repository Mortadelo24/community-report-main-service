from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from .links import UserCommunityLink
from typing import TYPE_CHECKING
import uuid


if TYPE_CHECKING:
    from .community import Community

class UserBase(SQLModel):
    display_name: str | None = None
    email: EmailStr
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

class UserFirebase(SQLModel):
    id: str 
    display_name: str | None = None
    email: EmailStr


class UserPublic(UserBase):
    pass


class UserToken(UserPublic):
    pass

class User(UserBase, table=True):
    firebase_id: str | None = Field(default=None, index=True, unique=True)
    communities_joined: list["Community"] = Relationship(back_populates="members", link_model=UserCommunityLink)
    owned_communities: list["Community"] = Relationship(back_populates="owner")