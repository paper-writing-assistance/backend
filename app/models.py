from sqlmodel import Field, SQLModel
from pydantic import BaseModel


class GraphNodeBase(BaseModel):
    paper_id: str
    title: str


class GraphNode(GraphNodeBase):
    s_title: str


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


class Paper(BaseModel):
    id: str
    abstract: str | None= None
    body: list[PaperBody] | None = None
    impact: int | None = None
    summary: PaperSummary | None = None
    published_year: str | None = None
    reference: list[str] | None = None
    figures: list[PaperFigure] | None = None
    tables: list[PaperFigure] | None = None
    title: str | None = None


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
