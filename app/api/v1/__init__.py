from fastapi import APIRouter

from app.api.v1.auth import authentication_router
from app.api.v1.posts import posts_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(authentication_router)
api_v1_router.include_router(posts_router)
