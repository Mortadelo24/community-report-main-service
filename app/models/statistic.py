from sqlmodel import SQLModel
from uuid import UUID


class StatisticReport(SQLModel):
    id: UUID
    text: str
    count: int


