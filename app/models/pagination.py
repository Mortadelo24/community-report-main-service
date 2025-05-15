from sqlmodel import SQLModel, Field


class Pagination(SQLModel):
    limit: int = Field(10, le=20)
    offset: int = Field(0, ge=0)

