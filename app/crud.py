# import uuid

# from sqlmodel import Session, select, or_, text

# import app.utils as utils
# from app.model.db import Paper, References


# # =========================================================
# # Paper
# # =========================================================
# def create_paper(session: Session, texts: dict) -> Paper:
#     embedding = utils.create_embedding(texts).detach()
#     paper = Paper(
#         title=(texts.get("title") or ""),
#         normalized_title=utils.normalize_text(texts.get("title") or ""),
#         embedding=embedding
#     )
#     session.add(paper)
#     session.commit()
#     session.refresh(paper)
#     return paper


# def get_papers_by_similarity(session: Session, query: dict) -> list[Paper]:
#     query_emb = utils.create_embedding(query).detach()
#     stmt = (select(Paper)
#             .order_by(Paper.embedding.cosine_distance(query_emb))
#             .limit(5))
#     result = session.exec(stmt).all()
#     return result


# def get_paper_by_id(session: Session, paper_id: str) -> Paper:
#     stmt = select(Paper).where(Paper.id == paper_id)
#     result = session.exec(stmt).one()
#     return result


# # =========================================================
# # References
# # =========================================================
# def create_reference(
#     session: Session, paper_id: uuid.UUID, ref_paper_id: uuid.UUID
# ) -> References:
#     reference = References(paper_id=paper_id, referenced_paper_id=ref_paper_id)
#     session.add(reference)
#     session.commit()
#     session.refresh(reference)
#     return reference


# def get_references_order_by_similarity(
#     session: Session, paper_id: uuid.UUID, num_retrieval: int
# ) -> list:
#     paper: Paper = get_paper_by_id(session, paper_id)
#     embedding = paper.embedding
    
#     # stmt = (select(References)
#     #         .join(Paper)
#     #         .where(or_(References.paper_id == paper_id, 
#     #                    References.referenced_paper_id == paper_id))
#     #         .order_by(Paper.embedding.cosine_distance(embedding))
#     #         .limit(num_retrieval))
    
#     stmt = text(
#         f"""
#         SELECT referencing_paper_id id FROM references r 
#         JOIN paper p ON r.id = p.id 
#         WHERE r.id = '{str(paper_id)}'

#         UNION

#         SELECT paper_id id FROM references r 
#         JOIN paper p ON r.id = p.id 
#         WHERE r.id = '{str(paper_id)}'

#         ORDER BY embedding <=> (
#             SELECT embedding FROM paper WHERE id = '{str(paper_id)}')

#         LIMIT {num_retrieval};
#         """
#     )
    
#     result = session.exec(stmt).all()
#     return result
