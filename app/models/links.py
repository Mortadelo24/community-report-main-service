from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4


class UserCommunityLink(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    community_id: UUID = Field(foreign_key="community.id", primary_key=True)