from fastapi import APIRouter, status, HTTPException, Depends, Path
from sqlmodel import select, col
from typing import Annotated
from ..models.token import TokenCreate, TokenResponse
from ..apis import firebase
from ..database import DBSessionDependency
from ..models.user import User, UserToken, UserResponse
from ..models.community import CommunityPublic, Community
from ..security import encode_user_token
from ..dependencies import user_token_dependency, current_user_dependency, get_same_user_id_path, get_current_user, get_user_token

router = APIRouter()

@router.post(
        "/token/validate",
        response_model=None,
        status_code=status.HTTP_202_ACCEPTED,
        summary="Raise a http exception if the token is invalid",
        dependencies=[Depends(get_user_token)]
)
def validate_token():
    return

@router.post(
        "/token", 
        response_model=TokenResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Creates a Bearer token",
        description="Creates a Bearer token from provider token",
        response_description="The bearer token that authenticates the user in this api"
)
def create_token(token: TokenCreate, session: DBSessionDependency):
    userFirebase = firebase.get_user(token.access_token)
    if not userFirebase:
        raise HTTPException(status_code=400, detail="Invalid access_token")  
    print(userFirebase.id)

# look for the user with the firebase id and if there is none create it
    statement = select(User).where(col(User.firebase_id) == userFirebase.id)
    user = session.exec(statement).first()

    if not user:
        newUser = User(
            firebase_id=userFirebase.id,
            display_name=userFirebase.display_name,
            email=userFirebase.email
        )
        session.add(newUser)
        session.commit()
        session.refresh(newUser)
        user = newUser
 

    tokenResponse = TokenResponse(
        access_token=encode_user_token(UserToken(**user.model_dump())),
        token_type="Bearer"
    )
    
    return tokenResponse

@router.get(
        "/me",
        response_model=UserResponse,
        status_code=status.HTTP_200_OK,
        summary="Returns the current user information",
        description="Uses the bearer token for indentifying the current user and return it",
        response_description="The current user information",
)
def read_current_user(userToken: user_token_dependency, session: DBSessionDependency):
    user = session.get(User, userToken.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The token is not registered")

    return UserResponse(**user.model_dump())




@router.get(
        "/{user_id}",
        response_model=UserResponse,
        status_code=status.HTTP_200_OK,
        summary="Returns the user that matches the id",
        response_description="The user information",
)
def read_user(user_id: Annotated[int, Path()], session: DBSessionDependency):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find the user")

    return user
    



@router.get(
        "/{user_id}/communities/joined", 
        response_model=list[CommunityPublic],
        status_code=status.HTTP_200_OK,
        summary="Returns the joined communities of an user",
        response_description="A list of communities",
        dependencies=[Depends(get_same_user_id_path)]
)
def read_user_communities_joined(user: current_user_dependency): 
    return user.communities_joined

@router.get(
    "/{user_id}/communities/owned",
    response_model=list[CommunityPublic],
    status_code=status.HTTP_200_OK,
    summary="Returns the communities owned by the user",
    response_description="A list of communities",
    dependencies=[Depends(get_same_user_id_path)]
)
def read_user_owned_communities(user: current_user_dependency):
    return user.owned_communities