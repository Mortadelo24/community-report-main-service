from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class CommunityBase(BaseModel):
    name: str


class CommunityOut(CommunityBase):
    id: int


class Community(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
