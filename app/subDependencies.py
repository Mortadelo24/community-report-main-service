from uuid import UUID
from fastapi import HTTPException, status
from .database import DBSessionDependency
from .models.community import Community

def get_community(community_id: UUID, session: DBSessionDependency):
    community = session.get(Community, community_id)

    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot found the community")

    return community