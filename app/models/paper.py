import uuid
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


association_table = Table(
    "references",
    Base.metadata,
    Column("paper_id", ForeignKey("paper.id"), primary_key=True),
    Column("referencing_paper_id", ForeignKey("paper.id"), primary_key=True)
)


class Paper(Base):
    __tablename__ = "paper"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[Optional[str]]
    normalized_title: Mapped[str]
    embedding: Mapped[Optional[Vector]] = mapped_column(Vector(768))
    references: Mapped[list["Paper"]] = relationship(
        "Paper",
        secondary=association_table,
        primaryjoin=(id == association_table.c.paper_id),
        secondaryjoin=(id == association_table.c.referencing_paper_id),
        back_populates="referenced_by",
    )
    referenced_by: Mapped[list["Paper"]] = relationship(
        "Paper",
        secondary=association_table,
        primaryjoin=(id == association_table.c.referencing_paper_id),
        secondaryjoin=(id == association_table.c.paper_id),
        back_populates="references",
    )

    def __repr__(self) -> str:
        return f"Paper(id={self.id!r}, title={self.title!r}), normalized_title={self.normalized_title!r}"
