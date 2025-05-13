from fastapi import APIRouter, HTTPException, status, Response, UploadFile, Depends
from uuid import UUID
from ..database.config import DBSessionDependency
from ..models.image import Image, ImagePublic
from ..models.report import Report
from ..dependencies import get_report_from_query
from typing import Annotated


router = APIRouter()


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}


@router.get(
    "/evidences",
    summary="Return the images related to the report id",
    response_model=list[ImagePublic]
)
def read_images(report: Annotated[Report, Depends(get_report_from_query)]):
    return report.images


@router.post(
    "/evidence",
    status_code=status.HTTP_201_CREATED,
    summary="Save an image",
)
async def create_evidence_image(report: Annotated[Report, Depends(get_report_from_query)], file: UploadFile, session: DBSessionDependency):
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
    "/{image_id}",
    summary="returns the requested image"
)
def read_image(image_id: UUID, session: DBSessionDependency):
    image = session.get(Image, image_id)

    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find the image")

    return Response(content=image.data, media_type=image.content_type)


