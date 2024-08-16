import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

import app.utils as utils
from app.models.paper import Paper


# =========================================================
# Create
# =========================================================
def create_paper(session: Session, texts: dict, dummy: bool = False) -> Paper:
    embedding = None
    if not dummy:
        embedding = utils.create_embedding(texts).detach()
    
    paper = Paper(
        title=(texts.get("title") or ""),
        normalized_title=utils.normalize_text(texts.get("title") or ""),
        embedding=embedding
    )
    session.add(paper)
    session.commit()
    session.refresh(paper)
    return paper


# =========================================================
# Read
# =========================================================
def get_papers_by_similarity(
    session: Session, query: dict, num_retrieval: int
) -> list[Paper]:
    query_emb = utils.create_query_embedding(query).detach()
    stmt = (select(Paper)
            .where(Paper.embedding != None)
            .order_by(Paper.embedding.cosine_distance(query_emb))
            .limit(num_retrieval))
    result = session.scalars(stmt).all()
    return result


def get_paper_by_id(session: Session, paper_id: uuid.UUID) -> Paper | None:
    stmt = select(Paper).where(Paper.id == paper_id)
    result = session.scalar(stmt)
    return result


def get_paper_by_title(session: Session, title: str) -> Paper | None:
    norm_title = utils.normalize_text(title)
    stmt = select(Paper).where(Paper.normalized_title == norm_title)
    result = session.scalar(stmt)
    return result


def get_references_by_id(session: Session, paper_id: uuid.UUID) -> list[Paper]:
    ref_alias = aliased(Paper)
    ref_to_stmt = (select(Paper)
                   .join(Paper.references.of_type(ref_alias))
                   .where(ref_alias.id == paper_id)
                   .where(Paper.embedding != None))
    ref_to_result = session.scalars(ref_to_stmt).all()

    ref_by_stmt = (select(Paper)
                   .join(Paper.referenced_by.of_type(ref_alias))
                   .where(ref_alias.id == paper_id)
                   .where(Paper.embedding != None))
    ref_by_result = session.scalars(ref_by_stmt).all()
    
    return ref_to_result + ref_by_result


# =========================================================
# Update
# =========================================================
def update_paper(session: Session, texts: dict) -> Paper:
    # Find paper
    norm_title = utils.normalize_text(texts['title'])
    stmt = (select(Paper).where(Paper.normalized_title == norm_title))
    paper = session.scalar(stmt)

    # Update value
    embedding = utils.create_embedding(texts).detach()
    paper.title = texts['title']
    paper.embedding = embedding
    session.commit()
    session.refresh(paper)
    return paper
