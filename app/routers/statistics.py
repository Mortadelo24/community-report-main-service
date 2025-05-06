from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, and_
from ..models.complaint import Complaint
from ..models.report import Report
from ..models.statistic import StatisticReport
from ..dependencies import community_from_quary_dependency, user_token_dependency
from ..database.config import DBSessionDependency

router = APIRouter()


@router.get(
    path="/community/reports",
    summary="Returns the data necessary to display the graph",
    response_model=list[StatisticReport],
    response_description="A list of statistic reports"
)
def read_community_reports_statistics(session: DBSessionDependency, community: community_from_quary_dependency, user: user_token_dependency):
    if community.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not the owner")

    data = []
    complaints = session.exec(select(Complaint)).all()

    for complaint in complaints:
        reports = session.exec(select(Report).where(and_(Report.complaint_id == complaint.id, Report.community_id == community.id))).all()
        data.append(StatisticReport(
            id=complaint.id,
            text=complaint.text,
            count=len(reports)
        ))

    return data
