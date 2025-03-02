import asyncio
import sys
from typing import TYPE_CHECKING

from app.config import MySettings
from app.core.domain.post.exceptions import PostPayloadTooLargeError
from app.core.services.post_services.cache_service import user_posts_key
from app.core.services.post_services.schemas import PostSchema
from app.logger import CustomLogger

if TYPE_CHECKING:
    import uuid

    from aiocache import Cache

    from app.core.domain.post.protocols import PostRepositoryInterface


async def add_post_service(
    user_id: "uuid.UUID",
    text: str,
    posts_repo: "PostRepositoryInterface",
    cache: "Cache",
) -> "PostSchema":
    size_mb = sys.getsizeof(text) / 1024 / 1024

    if size_mb > MySettings.TEXT_SIZE_LIMIT_MB:
        raise PostPayloadTooLargeError(
            message=f"Post payload exceeds the maximum allowed size {MySettings.TEXT_SIZE_LIMIT_MB} MB"
        )
    try:
        new_post = await posts_repo.add_post(
            user_id=user_id,
            text=text,
        )

        async def add_post_cache():
            cache_key = user_posts_key(user_id)
            try:
                vals = await cache.get(cache_key)  # pyright: ignore
                if vals:
                    vals.append(new_post)
                else:
                    vals = [new_post]
                await cache.set(cache_key, vals, ttl=MySettings.CACHE_EXPIRE_MINUTES * 60)  # pyright: ignore
            except Exception:  # noqa: BLE001
                CustomLogger.get_logger().error("Error adding cache", exc_info=True)

        asyncio.create_task(add_post_cache())  # noqa: RUF006

        return PostSchema(id=new_post.id)

    except Exception as e:
        CustomLogger.get_logger().exception("An error occurred while adding a post")
        raise e
