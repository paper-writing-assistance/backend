from fastapi import APIRouter

from app.api.routes import search
from app.api.routes import upload


api_router = APIRouter()

api_router.include_router(
    router=search.router,
    prefix="/search",
    tags=["Search Papers"]
)
api_router.include_router(
    router=upload.router,
    prefix="/upload",
    tags=["Upload Papers"]
)
