import torch
from fastapi import APIRouter

import app.utils as utils
from app.api.deps import CollectionDep, SessionDep
from app.crud.metadata import *
from app.crud.paper import *
from app.models.schemas import (
    PaperQuery,
    PaperQueryResponse,
    PaperGraphRequest,
    PaperGraphResponse
)


router = APIRouter()


@router.post(
    path="/query",
    summary="Search top 5 papers based on query text", 
    response_model=list[PaperQueryResponse]
)
async def search_papers_by_query(
    body: PaperQuery,
    collection: CollectionDep,
    session: SessionDep
):
    # Retrieve papers based on cosine similarity
    papers: list[Paper] = get_papers_by_similarity(
        session=session,
        query=body.model_dump(),
        num_retrieval=5
    )

    # Fetch metadata of selected papers
    metadata = [
        get_metadata_by_id(collection, p.id).model_dump() | {'id': p.id} 
    for p in papers]
    
    return [PaperQueryResponse(**d) for d in metadata]


@router.post(
    path="/graph", 
    summary="Search subgraph nodes given root node", 
    response_model=list[PaperGraphResponse]
)
async def search_subgraph(
    body: PaperGraphRequest, 
    collection: CollectionDep,
    session: SessionDep
):
    # Retrieve a list of adjacent nodes
    ref_papers: list[Paper] = get_references_by_id(
        session=session,
        paper_id=body.root_id,
    )
    
    # Sort by cosine similarity with query embedding
    query_emb = utils.create_query_embedding(body.query.model_dump())
    scores = [
        {
            "id": p.id,
            "score": utils.cosine_similarity(
                query_emb,
                torch.from_numpy(p.embedding)
            )
        }
        for p in ref_papers
    ]
    scores.sort(reverse=True, key=lambda x: x["score"])
    scores[:body.num_nodes]

    # Fetch metadata of selected papers
    result = [
        get_metadata_by_id(collection, p['id']).model_dump() | p
    for p in scores]

    return [PaperGraphResponse(**d) for d in result]
