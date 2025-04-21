from sqlmodel import SQLModel, Field

class CommunityBase(SQLModel):
    name: str

class CommunityCreate(CommunityBase):
    pass

class CommunityResponse(CommunityBase):
    id: int

class Community(CommunityBase, table=True):
    id: int | None = Field(default=None, primary_key=True)