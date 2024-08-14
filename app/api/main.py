from fastapi import APIRouter

from app.api.routes import search


api_router = APIRouter()

api_router.include_router(
    router=search.router,
    prefix="/search",
    tags=["Search Papers"]
)
