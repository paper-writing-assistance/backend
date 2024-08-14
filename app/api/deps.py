from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import engine


def get_db() -> Generator[Session, None, None]:
    """
    PostgreSQL session.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
