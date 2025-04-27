from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from .community import Community

class InvitationBase(SQLModel):
    community_id: UUID

class InvitationPublic(InvitationBase):
    id: UUID

class InvitationCreate(InvitationBase):
    pass

class Invitation(InvitationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    community: Community = Relationship(back_populates="invitations")
    community_id: UUID = Field(foreign_key="community.id")