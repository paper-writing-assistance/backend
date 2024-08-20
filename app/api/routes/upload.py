from fastapi import APIRouter

from app.api.deps import CollectionDep, SessionDep
from app.crud.paper import *
from app.crud.metadata import *
from app.crud.status import *
from app.models.metadata import Metadata
from app.models.paper import Paper
from app.models.schemas import *
from app.models.status import UploadStatus


router = APIRouter()


@router.post(
    path="/paper",
    summary="Upload new paper to database",
    response_model=PaperBase
)
async def upload_paper(
    body: Metadata,
    collection: CollectionDep,
    session: SessionDep,
):
    data = Metadata.model_validate(body)
    
    # Create paper
    paper: Paper = get_paper_by_title(session, data.title)
    if not Paper:
        paper = create_paper(
            session=session,
            texts={'title': data.title, 'abstract': data.abstract},
        )
    else:
        paper = update_paper(
            session=session,
            texts={'title': data.title, 'abstract': data.abstract},
        )

    # Create metadata
    create_metadata(
        collection=collection,
        id=paper.id,
        data=data
    )

    # Create references
    for ref_title in data.reference:
        ref_paper: Paper = create_paper(
            session=session,
            texts={'title': ref_title},
            dummy=True
        )
        paper.references.append(ref_paper)
    session.commit()

    return PaperBase(id=paper.id, title=data.title)


@router.get(
    path="/status/all",
    summary="Get upload status of all papers",
    response_model=list[UploadStatusSchema]
)
def get_upload_status(
    session: SessionDep
):
    return get_all_upload_status(session)


@router.post(
    path="/status",
    summary="Create upload status of given paper",
    response_model=UploadStatusSchema
)
def post_upload_status(
    session: SessionDep,
    body: UploadStatusCreate
):
    return create_upload_status(session, body.filename)


@router.put(
    path="/status",
    summary="Update upload status of given paper"
)
def put_upload_status(
    session: SessionDep,
    status_data: UploadStatusSchema
):
    new_status = UploadStatus(**status_data.model_dump())
    updated_status = update_upload_status(session, new_status)
    return UploadStatusSchema(**updated_status.to_dict())
