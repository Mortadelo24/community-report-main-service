from typing import Annotated
import uuid
from uuid import UUID

from fastapi import Depends, HTTPException, Path, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from .database.config import DBSessionDependency
from .models.community import Community
from .models.user import User, UserToken
from .models.report import Report
from .security import decode_user_token, security
from .subDependencies import get_community


def get_user_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        return decode_user_token(credentials.credentials)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")


user_token_dependency = Annotated[UserToken, Depends(get_user_token)]


def get_current_user(userToken: user_token_dependency, session: DBSessionDependency):
    user = session.get(User, userToken.id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return user


current_user_dependency = Annotated[User, Depends(get_current_user)]


def get_same_user_id_path(user_id: Annotated[uuid.UUID, Path()], user: user_token_dependency):

    if user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't read others communities")
    return user_id


same_user_id_path = Annotated[int, Depends(get_same_user_id_path)]

# community dependencies


def get_community_from_path(community_id: Annotated[uuid.UUID, Path()], session: DBSessionDependency):
    return get_community(community_id, session)


community_from_path_dependecy = Annotated[Community, Depends(get_community_from_path)]


def get_community_from_quary(community_id: Annotated[uuid.UUID, Query()], session: DBSessionDependency):
    return get_community(community_id, session)


community_from_quary_dependency = Annotated[Community, Depends(get_community_from_quary)]

# report dependencies


def get_report_from_query(report_id: Annotated[UUID, Query()], session: DBSessionDependency):
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find the report")

    return report


