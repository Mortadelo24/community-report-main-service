from fastapi import APIRouter, status, HTTPException
from ..models.report import ReportPublic, ReportCreate, Report
from ..dependencies import community_from_quary_dependency, current_user_dependency, user_token_dependency, filter_query_dependency
from ..database.config import DBSessionDependency
from uuid import UUID
from sqlmodel import select

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
    "/{report_id}",
    summary="Returns information about a report",
    response_description="A report",
    response_model=ReportPublic
)
def read_report(report_id: UUID, session: DBSessionDependency):
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find the report")

    return report


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Return the reports for a given community",
    response_model=list[ReportPublic],
    response_description="A list of reports"
)
def read_reports(community: community_from_quary_dependency, filter_query: filter_query_dependency, user: user_token_dependency, session: DBSessionDependency):
    if community.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not the owner")

    statement = select(Report).where(Report.community_id == community.id).offset(filter_query.offset).limit(filter_query.limit)
    reports = session.exec(statement).all()

    return reports


