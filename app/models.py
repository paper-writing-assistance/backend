from datetime import datetime

from numpy import ndarray
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, ConfigDict


class GraphNodeBase(BaseModel):
    paper_id: str
    title: str


class GraphNode(GraphNodeBase):
    s_title: str


class Vector(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str
    embedding: ndarray


class PaperBody(BaseModel):
    paragraph_id: int
    section: str
    text: str


class PaperFigure(BaseModel):
    idx: int
    name: str
    caption: str
    related: list[int]
    summary: str


class PaperQuery(BaseModel):
    domain: str
    problem: str
    solution: str


class PaperSummary(PaperQuery):
    keywords: list[str]


class PaperBase(BaseModel):
    id: str
    title: str | None = None


class PaperInference(PaperBase):
    abstract: str | None = None
    body: list[PaperBody] | None = None
    impact: int | None = None
    published_year: str | None = None
    reference: list[str] | None = None
    figures: list[PaperFigure] | None = None
    tables: list[PaperFigure] | None = None
    authors: list[str] | None = None


class Paper(PaperInference):
    summary: PaperSummary | None = None


class PaperCore(PaperBase):
    published_year: str | None = None
    summary: PaperSummary | None = None
    impact: int | None = None
    authors: list[str] | None = None


class PaperGraph(BaseModel):
    num_nodes: int
    root_id: str
    query: PaperQuery


class PaperScore(PaperCore):
    score: float


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int | None = None
    exp: int | None = None


class UserBase(SQLModel):
    username: str = Field(unique=True)
    full_name: str | None = None


class User(UserBase, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_admin: bool = False


class UserRegister(UserBase):
    password: str


class UploadStatusCreate(BaseModel):
    filename: str


class UploadStatus(SQLModel, table=True):
    request_id: int | None = Field(default=None, primary_key=True)
    filename: str
    requested_date: datetime | None = Field(
        default_factory=lambda: datetime.now())
    pdf_uploaded: bool = False
    bbox_detected: bool = False
    metadata_parsed: bool = False
    images_uploaded: bool = False
    keywords_extracted: bool = False
    metadata_stored: bool = False


class UpdateUploadStatus(BaseModel):
    request_id: int
    pdf_uploaded: bool | None = None
    bbox_detected: bool | None = None
    metadata_parsed: bool | None = None
    images_uploaded: bool | None = None
    keywords_extracted: bool | None = None
    metadata_stored: bool | None = None
    