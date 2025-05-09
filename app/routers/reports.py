from fastapi import APIRouter, Path, status, HTTPException, UploadFile, Response
from ..models.report import ReportPublic, ReportCreate, Report
from ..models.image import Image
from ..dependencies import community_from_quary_dependency, current_user_dependency, user_token_dependency
from ..database.config import DBSessionDependency
from typing import Annotated
from uuid import UUID

router = APIRouter()

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}


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


@router.post(
    "/{report_id}/evidence",
    status_code=status.HTTP_201_CREATED,
    summary="Save an image",
)
async def create_evidence_image(report_id: Annotated[UUID, Path()], file: UploadFile, session: DBSessionDependency):
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find the report")
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong image type")

    content = await file.read()
    new_image = Image(data=content, content_type=file.content_type)
    session.add(new_image)
    report.images.append(new_image)

    try:
        session.commit()
        session.refresh(new_image)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="could not create the image")

    return Response(content=new_image.data, media_type=new_image.content_type)


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


