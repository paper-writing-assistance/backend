import uuid

from pydantic import BaseModel


# =========================================================
# Paper
# =========================================================
class PaperBase(BaseModel):
    id: uuid.UUID
    title: str | None = None


class PaperQuery(BaseModel):
    domain: str
    problem: str | None = None
    solution: str | None = None


class PaperSummary(PaperQuery):
    keywords: list[str]


class PaperQueryResponse(PaperBase):
    published_year: str | None = None
    summary: PaperSummary | None = None
    impact: int | None = None
    authors: list[str] | None = None


class PaperGraphRequest(BaseModel):
    num_nodes: int
    root_id: str
    query: PaperQuery


class PaperGraphResponse(PaperQueryResponse):
    score: float


# =========================================================
# Upload Status
# =========================================================
class UploadStatusSchema(BaseModel):
    request_id: int
    filename: str
    pdf_upload: bool
    document_layout: bool
    reading_order: bool
    db_loaded: bool


class UploadStatusCreate(BaseModel):
    filename: str
