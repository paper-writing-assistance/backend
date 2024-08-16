from pymongo import MongoClient
from pymongo.collection import Collection
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# PostgreSQL
engine: Engine = create_engine(str(settings.SQLALCHEMY_DATABSE_URI), echo=True)
Base = declarative_base()

# MongoDB
client = MongoClient(
    str(settings.MONGO_CONNECTION_STRING),
    uuidRepresentation='standard',
)
collection: Collection = (client
                          .get_database(settings.MONGO_DATABASE)
                          .get_collection(settings.MONGO_COLLECTION))
