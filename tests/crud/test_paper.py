import pytest
from sqlalchemy.orm import Session
from app.models.paper import Base, Paper

from app.core.database import engine
from app.crud.paper import *


@pytest.fixture(name="session")
def session_fixture():
    with Session(engine) as session:
        yield session


def test_create_paper(session: Session):
    texts = {
        'title': 'BERT', 
        'abstract': 'We introduce a new language representation model'
    }
    paper: Paper = create_paper(session, texts)

    dummy_texts = {'title': 'GPT-3'}
    dummy_paper: Paper = create_paper(session, dummy_texts, dummy=True)

    assert type(paper) == Paper
    assert paper.id is not None
    assert len(paper.embedding) == 768
    assert dummy_paper.embedding is None


def test_get_papers_by_similarity(session: Session):
    query = {
        'title': 'BERT', 
        'abstract': 'We introduce a new language representation model'
    }

    num_retrieval = 5
    result = get_papers_by_similarity(session, query, num_retrieval)

    assert type(result) == list
    # assert len(result) == num_retrieval
    for elem in result:
        assert type(elem) == Paper


def test_get_paper_by_id(session: Session):
    texts = {
        'title': 'BERT', 
        'abstract': 'We introduce a new language representation model'
    }
    paper = create_paper(session, texts)
    result = get_paper_by_id(session, paper.id)

    assert type(result) == Paper
    assert result.id == paper.id


def test_get_references_by_id(session: Session):
    p1 = create_paper(session, {'title': 'paper 1'})
    p2 = create_paper(session, {'title': 'paper 2'})
    p3 = create_paper(session, {'title': 'paper 3'})
    p4 = create_paper(session, {'title': 'paper 4'})
    p5 = create_paper(session, {'title': 'paper 5'})

    session.add_all([p1, p2, p3, p4, p5])
    p1.references.append(p2)
    p2.references.append(p3)
    p2.references.append(p4)
    session.commit()
    
    result = get_references_by_id(session, p2.id)
    
    assert set(result) == {p1, p3, p4}
