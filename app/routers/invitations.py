from fastapi import APIRouter, status, Body, HTTPException
from ..models.invitation import InvitationPublic, InvitationCreate, Invitation, InvitationJoin
from ..models.community import CommunityPublic
from typing import Annotated
from ..database.config import DBSessionDependency
from ..dependencies import community_from_quary_dependency, current_user_dependency, user_token_dependency

router = APIRouter()


@router.post(
    "/",
    response_model=InvitationPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Creates an invitation",
    response_description="The invitation",
)
def create_invitation(invitationCreate: Annotated[InvitationCreate, Body()], user: current_user_dependency, session: DBSessionDependency):
    newInvitation = Invitation(user_id=user.id, **invitationCreate.model_dump())
    session.add(newInvitation)

    try:
        session.commit()
        session.refresh(newInvitation)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="could not create the invitaion")

    return newInvitation


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Returns the invitations for a given community",
    response_model=list[InvitationPublic],
    response_description="A list of invitations",
)
def read_invitations(community: community_from_quary_dependency, user: user_token_dependency):
    if community.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner")

    return community.invitations


@router.post(
    "/join",
    response_model=CommunityPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Add the user to the community referenced by the invitation",
    response_description="The community the user has joined"
)
def join_community(user: current_user_dependency, invitationJoin: InvitationJoin, session: DBSessionDependency):
    invitation = session.get(Invitation, invitationJoin.id)

    if not invitation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can not find the invitation")

    community = invitation.community

    community.members.append(user)

    session.add(community)

    try:
        session.commit()
        session.refresh(community)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not join the community")

    return invitation.community
