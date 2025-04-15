from fastapi import FastAPI, Depends, Header, HTTPException
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from firebase import get_firebase_user, initialize_firebase, get_firebase_uid
from pydantic import BaseModel


class User(BaseModel):
    id: str
    display_name: str | None = None


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
                display_name=userInfo.display_name
            )


@app.get("/")
def read_root(uid: Annotated[str, Depends(get_uid)]):
    return uid


@app.get("/users/me")
def read_user_me(user: Annotated[User, Depends(get_current_user)]):
    return user


@app.get("/items/{item_id}", )
def read_item(item_id: int, q: str | None):
    return {"item_id": item_id, "q": q}
