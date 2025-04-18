from fastapi import FastAPI, HTTPException, Body, Depends, Path
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database import create_db_and_tables, DBSessionDependency
from data_parsers import get_user_from_firebase
from apis.firebase import initialize_firebase, get_firebase_uid

from models.user import User, UserOut, UserAuth
from models.community import CommunityOut

from enum import Enum
from sqlmodel import select
from auth.tokens import encode_user_token, decode_user_token

app = FastAPI()

origins = ["http://localhost:5173", "https://integrador-community.netlify.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"]
)

security = HTTPBearer()


class AuthProvider(str, Enum):
    google = "google"


def get_user_from_provider(provider: Annotated[AuthProvider, Body(embed=True)], token: Annotated[str, Body(embed=True)],
                           DBSession: DBSessionDependency):
    if provider != "google":
        raise HTTPException(status_code=400, detail="Only google is implemented")

    firebase_id = get_firebase_uid(token)

    if not firebase_id:
        raise HTTPException(status_code=400, detail="Invalid firebase token")

    user = DBSession.exec(select(User).where(User.firebase_id == firebase_id)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Bad credentials")

    return user


def get_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        deconded_user = decode_user_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Auth Token")

    return UserAuth(**deconded_user)


def auth_dependency(user: Annotated[UserAuth, Depends(get_user_from_provider)], DBSession: DBSessionDependency):
    userInDB = DBSession.exec(select(User).where(User.id == user.id)).first()
    if not userInDB:
        raise HTTPException(status_code=400, detail="Bad credentials")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    initialize_firebase()


@app.get("/")
def read_root():
    return "A default root"


@app.post("/login")
def login(user: Annotated[User, Depends(get_user_from_provider)]):
    userAuth = UserAuth(**user.dict())
    encoded_user_token = encode_user_token(userAuth)
    return {
        "accessToken": encoded_user_token
    }


@app.get("/users/me", response_model=UserOut)
def read_current_user(user: Annotated[UserAuth, Depends(get_user)]):
    return user


@app.post("/users")
async def create_user(provider: Annotated[AuthProvider, Body(embed=True)], token: Annotated[str, Body(embed=True)], DBSession: DBSessionDependency):
    try:
        userIn = get_user_from_firebase(token)
    except Exception:
        HTTPException(status_code=400, detail="Invalid firebase token")

    newUser = User(**userIn.dict())

    try:
        DBSession.add(newUser)
        DBSession.commit()
        DBSession.refresh(newUser)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not process NewUser")

    userAuth = UserAuth(**newUser.dict())

    return {
        "accessToken": encode_user_token(userAuth)
    }


@app.get("/users/{uid}/communities", response_model=list[CommunityOut])
async def read_user_communities(uid: Annotated[int, Path()]):
    print(f"communities for {uid}")
    fake_community = CommunityOut(id=2, name="Fake community")
    return [fake_community]