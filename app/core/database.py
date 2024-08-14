from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# PostgreSQL
engine: Engine = create_engine(str(settings.SQLALCHEMY_DATABSE_URI), echo=True)
Base = declarative_base()
