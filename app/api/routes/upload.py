from fastapi import APIRouter

from app.api.deps import CollectionDep, SessionDep
from app.crud.paper import *
from app.crud.metadata import *
from app.models.metadata import Metadata
from app.models.paper import Paper
from app.models.schemas import *


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
