from fastapi import APIRouter, status, Body, HTTPException
from ..models.invitation import InvitationPublic, InvitationCreate, Invitation
from ..models.community import Community, CommunityPublic
from typing import Annotated
from ..database import DBSessionDependency


router = APIRouter()

@router.post(
    "/",
    response_model=InvitationPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Creates an invitation",
    response_description="The invitation"
)
def create_invitation(invitationCreate: Annotated[InvitationCreate, Body()], session: DBSessionDependency):
    newInvitation = Invitation.model_validate(invitationCreate)
    session.add(newInvitation)

    try:
        session.commit()
        session.refresh(newInvitation)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="could not create the invitaion")

    return newInvitation

@router.post(
    "/join",
    response_model=CommunityPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Add the user to the community referenced by the invitation",
    response_description="The community the user has joined"
) 
def join_community():
    # todo add the user to the community
    return
