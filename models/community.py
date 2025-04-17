from pydantic import BaseModel


class CommunityBase(BaseModel):
    name: str


class CommunityOut(CommunityBase):
    id: int
