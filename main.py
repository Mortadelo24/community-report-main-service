from fastapi import FastAPI, Depends, Header, HTTPException, Path
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from firebase import get_firebase_user, initialize_firebase, get_firebase_uid
from pydantic import BaseModel


class User(BaseModel):
    id: str
    display_name: str | None = None
    photo_url: str | None = None


class Community(BaseModel):
    id: str
    name: str


initialize_firebase()
app = FastAPI()

origins = [
        "http://localhost:5173",
        ]
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST", "GET", "PUT", "DELETE"],
        allow_headers=["*"]
        )


async def get_uid(Authorization: Annotated[str, Header()]):
    uid = get_firebase_uid(Authorization)

    if not uid:
        raise HTTPException(status_code=400,
                            detail="Authorization token invalid")
    return uid


async def get_current_user(uid: Annotated[str, Depends(get_uid)]):
    userInfo = await get_firebase_user(uid)
    return User(
                id=userInfo.uid,
                display_name=userInfo.display_name,
                photo_url=userInfo.photo_url
            )


async def verify_user_id(user_id: Annotated[str, Path()]):
    if not await get_firebase_user(user_id):
        raise HTTPException(status_code=400, detail="Invalid user: " + user_id)
    return user_id


@app.get("/")
def read_root(uid: Annotated[str, Depends(get_uid)]):
    return uid


@app.get("/users/me")
def read_user_me(user: Annotated[User, Depends(get_current_user)]):
    return user


@app.get("/users/{user_id}/communities")
def read_communities(user_id: Annotated[str, Depends(verify_user_id)],
                     current_user_id: Annotated[str, Depends(get_uid)]):

    fake_communities = [
            {"id": "faffdfafad", "name": "prueba 2"}
            ]

    return fake_communities
