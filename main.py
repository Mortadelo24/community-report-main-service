from fastapi import FastAPI, HTTPException, Body, Depends
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, DBSessionDependency
from data_parsers import get_user_from_firebase
from firebase import initialize_firebase, get_firebase_uid
from models.user import User, UserOut
from enum import Enum
from sqlmodel import select
from auth.tokens import encode_user_token, decode_user_token

app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"]
)


class AuthProvider(str, Enum):
    google = "google"


def get_authenticated_user(provider: Annotated[AuthProvider, Body(embed=True)], token: Annotated[str, Body(embed=True)],
                           DBSession: DBSessionDependency):
    if provider != "google":
        raise HTTPException(status_code=400, detail="Only google is implemented")

    firebase_id = get_firebase_uid(token)

    if not firebase_id:
        raise HTTPException(status_code=400, detail="Invalid firebase token")

    try:
        user = DBSession.exec(select(User).where(User.firebase_id == firebase_id)).first()
    except Exception:
        raise HTTPException(status_code=400, detail="Bad credentials")

    return user


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    initialize_firebase()


@app.post("/login")
def login(user: Annotated[User, Depends(get_authenticated_user)]):
    userOut = UserOut(**user.dict())
    encoded_user_token = encode_user_token(userOut)
    return encoded_user_token


@app.post("/users")
async def create_user(DBSession: DBSessionDependency,
                      firebase_token: Annotated[str | None, Body(embed=True)] = None):
    userIn = None
    # TODO: change the way the token is handle and the providers like login
    if firebase_token:
        userIn = get_user_from_firebase(firebase_token)
    else:
        raise HTTPException(status_code=400, detail="The body should contain a method")

    newUser = User(**userIn.dict())

    try:
        DBSession.add(newUser)
        DBSession.commit()
        DBSession.refresh(newUser)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not process NewUser")

    return newUser
