import uuid

import pytest
from sqlalchemy.orm import Session
from app.models.status import UploadStatus

from app.core.database import engine
from app.crud.status import *


@pytest.fixture(name="session")
def session_fixture():
    with Session(engine) as session:
        yield session

def test_create_upload_status(session: Session):
    filename = "Attention is All You Need"
    status = create_upload_status(session, filename)
    
    assert type(status) == UploadStatus
    assert status.filename == filename
    assert status.pdf_upload == False


def test_get_all_upload_status(session: Session):
    s1 = create_upload_status(session, "req 1")
    s2 = create_upload_status(session, "req 2")
    
    all_status = get_all_upload_status(session)

    assert s1 in all_status
    assert s2 in all_status


def test_update_upload_status(session: Session):
    s1 = create_upload_status(session, str(uuid.uuid4()))
    s1.pdf_upload = True
    s1.reading_order = True

    s1_new = update_upload_status(session, s1)

    assert s1.request_id == s1_new.request_id
    assert s1_new.pdf_upload == True
    assert s1_new.reading_order == True
