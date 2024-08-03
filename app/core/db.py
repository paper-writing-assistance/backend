from pinecone import Pinecone, Index
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sqlmodel import create_engine

from app.core.config import settings

# PostgreSQL
engine = create_engine(str(settings.SQLALCHEMY_DATABSE_URI))

# MongoDB
client = MongoClient(settings.MONGO_URI, server_api=ServerApi("1"))
database = client[settings.MONGO_DATABASE]
collection = database[settings.MONGO_COLLECTION]

# Pinecone
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

class PineconeIndex:
    domain: Index = pc.Index(settings.PINECONE_INDEX_DOMAIN)
    domain_problem: Index = pc.Index(settings.PINECONE_INDEX_DOMAIN_PROBLEM)
    domain_solution: Index = pc.Index(settings.PINECONE_INDEX_DOMAIN_SOLUTION)
    domain_problem_solution: Index = pc.Index(
        settings.PINECONE_INDEX_DOMAIN_PROBLEM_SOLUTION)
    
index = PineconeIndex()
