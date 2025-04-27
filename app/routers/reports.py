from fastapi import APIRouter, status, HTTPException
from ..models.report import ReportPublic, ReportCreate, Report
from typing import Annotated
from uuid import UUID

from ..dependencies import community_from_quary_dependency, current_user_dependency

from ..database import DBSessionDependency

router = APIRouter()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Creates a report",
    response_model=ReportPublic,
    response_description="The created report"
)
def create_report(user: current_user_dependency , reportCreate: ReportCreate , session: DBSessionDependency):
    newReport = Report(
        user_id=user.id,
        community_id=reportCreate.community_id,
        complaint=reportCreate.complaint,
    )

    session.add(newReport)

    try:
        session.commit()
        session.refresh(newReport)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create the report")

    return newReport

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Return the reports for a given community",
    response_model=list[ReportPublic],
    response_description="A list of reports"
)
def read_reports(community:community_from_quary_dependency):
    return community.reports


@router.get(
    "/{report_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReportPublic,
    response_description="A report"
)
def read_report():
    #todo return the report id with new dependecy
    return