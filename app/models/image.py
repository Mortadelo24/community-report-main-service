from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class ImageBase(SQLModel):
    pass


class Image(ImageBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    data: bytes
    content_type: str
