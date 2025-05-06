from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database.config import create_db_and_tables
from contextlib import asynccontextmanager
from .routers import users, communities, reports, invitations, complaints, statistics
from .apis import firebase
from .dependencies import get_user_token


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
app.include_router(
    complaints.router,
    prefix="/complaints",
    tags=["complaints"],
    dependencies=[Depends(get_user_token)]
)
app.include_router(
    statistics.router,
    prefix="/statistics",
    tags=["statistics"],
    dependencies=[Depends(get_user_token)]
)

app.include_router(
    communities.router,
    prefix="/communities",
    tags=["communities"],
    dependencies=[Depends(get_user_token)]
)
app.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"],
    dependencies=[Depends(get_user_token)]
)
app.include_router(
    invitations.router,
    prefix="/invitations",
    tags=["Invitations"],
    dependencies=[Depends(get_user_token)]
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
