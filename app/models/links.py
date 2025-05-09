from sqlmodel import Field, SQLModel
from uuid import UUID


class UserCommunityLink(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    community_id: UUID = Field(foreign_key="community.id", primary_key=True)


class ReportImageLink(SQLModel, table=True):
    report_id: UUID = Field(foreign_key="report.id", primary_key=True)
    image_id: UUID = Field(foreign_key="image.id", primary_key=True)
