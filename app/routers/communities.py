from fastapi import APIRouter, status, HTTPException, Path
from typing import Annotated


from ..database import DBSessionDependency
from ..models.community import CommunityPublic, CommunityCreate, Community
from ..models.user import User, UserPublic
from ..dependencies import user_token_dependency, community_from_path_dependecy, current_user_dependency
from ..models.report import Report

router = APIRouter()

@router.post(
    "/",
    response_model=CommunityPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Creates a community", 
    description="Creates a community with the information provided",
    response_description="The community that was created"
)
def create_community(communityCreate: CommunityCreate, owner: current_user_dependency, session: DBSessionDependency):
    communityCreateDict =  communityCreate.model_dump()
    communityCreateDict["owner_id"] = owner.id

    
    newCommunity = Community.model_validate(communityCreateDict)
    
    newCommunity.members.append(owner)
    
    session.add(newCommunity)

    try: 
        session.commit() 
        session.refresh(newCommunity)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="could not create the community")

    return newCommunity

@router.get(
    "/{community_id}",
    response_model=CommunityPublic,
    status_code=status.HTTP_200_OK,
    summary="Returns the requested community",
    description="...",
    response_description="The community requested"
)
def read_community(community: community_from_path_dependecy):
    return community

@router.get(
        "/{community_id}/members",
        response_model=list[UserPublic],
        status_code=status.HTTP_200_OK,
        summary="Returns the community's members",
        response_description="A list of Users", 
)
def read_communities(community: community_from_path_dependecy):
     
    return community.members


