from fastapi import APIRouter, status, HTTPException, Depends, Path
from sqlmodel import select, col
from typing import Annotated
from ..models.token import TokenCreate, TokenResponse
from ..apis import firebase
from ..database import DBSessionDependency
from ..models.user import User, UserToken, UserResponse
from ..models.community import CommunityResponse
from ..security import encode_user_token
from ..dependencies import user_token_dependency

router = APIRouter()

@router.post(
        "/token", 
        response_model=TokenResponse,
        status_code=status.HTTP_201_CREATED,
        summary="Creates a Bearer token",
        description="Creates a Bearer token from provider token",
        response_description="The bearer token that authenticates the user in this api"
)
def create_token(token: TokenCreate, session: DBSessionDependency):
    firebase.initialize()
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
        response_description="The current user information"
)
def read_current_user(userToken: user_token_dependency, session: DBSessionDependency):
    user = session.get(User, userToken.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The token is not registered")

    return UserResponse(**user.model_dump())


@router.get(
        "/{user_id}/communities", 
        response_model=list[CommunityResponse],
        status_code=status.HTTP_200_OK,
        summary="Returns the communities of an user",
        description="Makes a request to the data base for the communities of a specific user_id",
        response_description="The communities of the given user_id"
)
def read_user_communities(user_id: Annotated[int, Path()] , userToken: user_token_dependency):
    if user_id != userToken.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't read others communities")
    
    fake_community = CommunityResponse(name="this is fake", id= 2 )
    return [fake_community]