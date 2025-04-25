from typing import Annotated
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import HTTPAuthorizationCredentials
import uuid

from .security import security, decode_user_token
from .models.user import UserToken, User
from .models.community import Community
from .database import DBSessionDependency

def get_user_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        return decode_user_token(credentials.credentials)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

user_token_dependency =  Annotated[UserToken, Depends(get_user_token)]

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


def get_community_from_path(community_id: Annotated[uuid.UUID, Path()],  session: DBSessionDependency):
    community = session.get(Community, community_id)

    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot found the community")

    return community

community_from_path_dependecy = Annotated[Community, Depends(get_community_from_path)]