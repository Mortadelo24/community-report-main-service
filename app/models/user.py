from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel

class UserBase(BaseModel):
    display_name: str | None = None
    email: EmailStr

class UserFirebase(UserBase):
    id: str 


class UserResponse(UserBase):
    id: int


class UserToken(UserResponse):
    pass

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    display_name: str | None = None
    firebase_id: str | None = Field(default=None, index=True, unique=True)
    email: EmailStr