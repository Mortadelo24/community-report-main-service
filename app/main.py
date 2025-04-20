from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables
from contextlib import asynccontextmanager
from .routers import users
from .apis import firebase

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables() 
    firebase.initialize() 
    yield

app = FastAPI(
    lifespan=lifespan
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    
)

origins = ["http://localhost:5173", "https://integrador-community.netlify.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return "cerru is real"

@app.get("/health")
def read_health():
    return 