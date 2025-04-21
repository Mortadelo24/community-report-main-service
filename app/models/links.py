from sqlmodel import Field, SQLModel

class UserCommunityLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="community.id", primary_key=True)