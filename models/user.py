from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class UserBase(BaseModel):
    display_name: str | None = None
    email: str


class UserIn(UserBase):
    firebase_id: str | None = None


class UserOut(UserBase):
    id: int


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    display_name: str | None = Field(default=None)
    firebase_id: str | None = Field(default=None, index=True, unique=True)
    email: str = Field()
