from fastapi import APIRouter, status, HTTPException, Path
from typing import Annotated


from ..database import DBSessionDependency
from ..models.community import CommunityResponse, CommunityCreate, Community

router = APIRouter()

@router.post(
    "/",
    response_model=CommunityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Creates a community", 
    description="Creates a community with the information provided",
    response_description="The community that was created"
)
def create_community(communityCreate: CommunityCreate, session: DBSessionDependency):
    newCommunity = Community(**communityCreate.model_dump())
    session.add(newCommunity)

    try: 
        session.commit() 
        session.refresh(newCommunity)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="could not create the community")

    return newCommunity

@router.get(
    "/{community_id}",
    response_model=CommunityResponse,
    status_code=status.HTTP_200_OK,
    summary="Returns the requested community",
    description="...",
    response_description="The community requested"
)
def read_community(community_id: Annotated[int, Path()], session: DBSessionDependency):
    community = session.get(Community, community_id)

    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can not found the community")
    
    return community