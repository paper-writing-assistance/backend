from pydantic import BaseModel


class Body(BaseModel):
    paragraph_id: int
    section: str
    text: str


class Figure(BaseModel):
    idx: int
    name: str
    caption: str
    related: list[int]
    summary: str


class Metadata(BaseModel):
    title: str
    abstract: str
    body: list[Body]
    impact: int
    published_year: str
    reference: list[str]
    figures: list[Figure]
    tables: list[Figure]
    authors: list[str]
