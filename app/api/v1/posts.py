import uuid
from typing import TYPE_CHECKING, Annotated

from aiocache import Cache
from fastapi import APIRouter, Depends
from fastapi.params import Param

import app.core.services.post_services as post_services
import app.core.services.post_services.schemas as post_schemas
from app.api.v1.decorators import cache_response
from app.api.v1.dependencies import get_cache_dependency, get_current_user, posts_repo_dependency
from app.config import MySettings

if TYPE_CHECKING:
    from app.core.domain.commons.session import SessionType
    from app.core.domain.post.protocols import PostRepositoryInterface
    from app.core.domain.user.entities import UserEntity

posts_router = APIRouter(
    prefix="/posts",
    tags=["POSTS"],
)


@posts_router.post("/add-post", response_model=post_schemas.PostSchema)
async def add_post(
    data: post_schemas.PostBase,
    user: Annotated["UserEntity", Depends(get_current_user)],
    posts_repo: Annotated["PostRepositoryInterface[SessionType]", Depends(posts_repo_dependency)],
) -> post_schemas.PostSchema:
    return await post_services.add_post_service(
        user=user,
        text=data.text,
        posts_repo=posts_repo,
    )


@posts_router.get("/get_my_posts", response_model=list[post_schemas.PostOutSchema])
@cache_response(ttl=MySettings.CACHE_EXPIRE_MINUTES * 60, namespace="user_posts")
async def get_all_my_post(
    user: Annotated["UserEntity", Depends(get_current_user)],
    posts_repo: Annotated["PostRepositoryInterface[SessionType]", Depends(posts_repo_dependency)],
    cache: Annotated[Cache, Depends(get_cache_dependency)],
) -> "list[post_schemas.PostOutSchema]":
    return await post_services.get_posts_service(
        user=user,
        posts_repo=posts_repo,
    )


@posts_router.delete("/delete_my_post", response_model=dict)
async def delete_my_post(
    user: Annotated["UserEntity", Depends(get_current_user)],
    post_id: Annotated[uuid.UUID, Param(...)],
    posts_repo: Annotated["PostRepositoryInterface[SessionType]", Depends(posts_repo_dependency)],
    cache: Annotated[Cache, Depends(get_cache_dependency)],
) -> dict:
    cache_key = f"user_posts:user:{user.id}"

    await post_services.detete_post_service(
        user=user,
        post_id=post_id,
        posts_repo=posts_repo,
    )
    await cache.delete(cache_key)  # pyright: ignore
    return {"status": "success"}
