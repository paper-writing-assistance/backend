from typing import Annotated, Generator

from fastapi import Depends
from pymongo.collection import Collection
from sqlalchemy.orm import Session

from app.core.database import engine, collection


def get_db() -> Generator[Session, None, None]:
    """
    PostgreSQL session.
    """
    with Session(engine) as session:
        yield session

    
def get_collection() -> Generator[Collection, None, None]:
    """
    MongoDB collection.
    """
    return collection


SessionDep = Annotated[Session, Depends(get_db)]
CollectionDep = Annotated[Collection, Depends(get_collection)]
