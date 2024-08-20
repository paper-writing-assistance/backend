from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UploadStatus(Base):
    __tablename__ = "upload_status"

    request_id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    pdf_upload: Mapped[bool] = mapped_column(default=False)
    document_layout: Mapped[bool] = mapped_column(default=False)
    reading_order: Mapped[bool] = mapped_column(default=False)
    db_loaded: Mapped[bool] = mapped_column(default=False)
