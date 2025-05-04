from fastapi import APIRouter, status, Path, HTTPException
from ..models.complaint import Complaint, ComplaintPublic
from typing import Annotated
from uuid import UUID
from ..database.config import DBSessionDependency
from sqlmodel import select


router = APIRouter()


@router.get(
    "/",
    summary="Return a list of all complaints",
    response_model=list[ComplaintPublic],
    response_description="A list of complaints"
)
def read_complaints(session: DBSessionDependency):
    statement = select(Complaint)
    complaints = session.exec(statement).all()

    return complaints


@router.get(
    "/{complaint_id}",
    status_code=status.HTTP_200_OK,
    summary="Return the complaint data",
    response_model=ComplaintPublic,
    response_description="The complaint object"
)
def read_complaint(complaint_id: Annotated[UUID, Path()], session: DBSessionDependency):
    print(complaint_id)
    complaint = session.get(Complaint, complaint_id)

    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find the complaint")

    return complaint

