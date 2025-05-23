from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from .preset import insertPresets

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
# add echo if you want to see the comands


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        insertPresets(session)


def get_db_session():
    with Session(engine) as session:
        yield session


DBSessionDependency = Annotated[Session, Depends(get_db_session)]
