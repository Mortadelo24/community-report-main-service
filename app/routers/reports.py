from fastapi import APIRouter, status, HTTPException
from ..models.report import ReportPublic, ReportCreate, Report, ReportChar
from ..models.complaint import Complaint
from ..dependencies import community_from_quary_dependency, current_user_dependency, user_token_dependency
from sqlmodel import select, and_
from ..database.config import DBSessionDependency

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Creates a report",
    response_model=ReportPublic,
    response_description="The created report"
)
def create_report(user: current_user_dependency, reportCreate: ReportCreate, session: DBSessionDependency):
    newReport = Report(
        user_id=user.id,
        community_id=reportCreate.community_id,
        complaint_id=reportCreate.complaint_id
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
def read_reports(community: community_from_quary_dependency, user: user_token_dependency):
    if community.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not the owner")

    return community.reports


@router.get(
    "/datachars",
    summary="A colection of data for a data char",
    response_model=list[ReportChar],
    response_description="A list of reports"
)
def read_datachar(session: DBSessionDependency, community: community_from_quary_dependency, user: user_token_dependency):
    if community.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not the owner")

    data = []
    complaints = session.exec(select(Complaint)).all()

    for complaint in complaints:
        reports = session.exec(select(Report).where(and_(Report.complaint_id == complaint.id, Report.community_id == community.id))).all()
        data.append(ReportChar(
            id=complaint.id,
            text=complaint.text,
            count=len(reports)
        ))

    return data



