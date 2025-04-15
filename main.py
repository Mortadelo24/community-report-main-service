from fastapi import FastAPI, Request
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from firebase import isAuthTokenValid, initialize_firebase


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


@app.middleware("http")
async def isTokenValid(request: Request, call_next):
    if "Authorization" in request.headers:
        print(isAuthTokenValid(request.headers["Authorization"]))
    return await call_next(request)


@app.get("/")
def read_root():
    return {"hello", "peru"}


@app.get("/items/{item_id}", )
def read_item(item_id: int, q: str | None):
    return {"item_id": item_id, "q": q}
