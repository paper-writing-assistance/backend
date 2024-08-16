from pydantic import AnyUrl, MongoDsn, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings

from app.core.embedding import *


class Settings(BaseSettings):

    PROJECT_NAME: str = "YOSO Service Backend"
    API_V1_STR: str = "/api/v1"

    BACKEND_CORS_ORIGINS: list[AnyUrl] | list[str] = ["*"]

    # PostgreSQL configurations
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def SQLALCHEMY_DATABSE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
        )
    
    # MongoDB configurations
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DATABASE: str = "you-only-search-once"
    MONGO_COLLECTION: str = "dev"

    @computed_field
    @property
    def MONGO_CONNECTION_STRING(self) -> MongoDsn:
        return MultiHostUrl.build(
            scheme="mongodb",
            host=self.MONGO_HOST,
            port=self.MONGO_PORT
        )
    
    # Embedding
    EMBEDDING_MODEL: Embedding = Specter2()
    

settings = Settings()
