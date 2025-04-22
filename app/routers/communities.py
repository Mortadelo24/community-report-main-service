from fastapi import APIRouter, status, HTTPException, Path
from typing import Annotated


from ..database import DBSessionDependency
from ..models.community import CommunityPublic, CommunityCreate, Community
from ..models.user import User
from ..dependencies import user_token_dependency

router = APIRouter()

@router.post(
    "/",
    response_model=CommunityPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Creates a community", 
    description="Creates a community with the information provided",
    response_description="The community that was created"
)
def create_community(communityCreate: CommunityCreate, userToken: user_token_dependency, session: DBSessionDependency):
    
    owner = session.get(User, userToken.id) 
    
    if not owner or not owner.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
 
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
def read_community(community_id: Annotated[int, Path()],  session: DBSessionDependency):
    community = session.get(Community, community_id)

    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can not found the community")
    
    return community

@router.post(
    "{community_id}/join",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    summary="add a user to the community",
    response_description="The community the user joined"
) 
def add_member_community():
    return None
