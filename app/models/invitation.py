from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from .community import Community
from .user import User

class InvitationBase(SQLModel):
    community_id: UUID

class InvitationPublic(InvitationBase):
    id: UUID
    user_id: UUID

class InvitationCreate(InvitationBase):
    pass

class InvitationJoin(SQLModel):
    id: UUID

class Invitation(InvitationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    community: Community = Relationship(back_populates="invitations")
    user: User = Relationship(back_populates="invitations")
    community_id: UUID = Field(foreign_key="community.id")
    user_id: UUID = Field(foreign_key="user.id")