from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.status import UploadStatus


# =========================================================
# Create
# =========================================================
def create_upload_status(session: Session, filename: str) -> UploadStatus:
    upload_status = UploadStatus(filename=filename)
    session.add(upload_status)
    session.commit()
    session.refresh(upload_status)
    return upload_status


# =========================================================
# Read
# =========================================================
def get_all_upload_status(session: Session) -> list[UploadStatus]:
    result = session.scalars(select(UploadStatus)).all()
    return result


# =========================================================
# Update
# =========================================================
def update_upload_status(session: Session, new: UploadStatus) -> UploadStatus:
    merged = session.merge(new)
    session.commit()
    return merged
