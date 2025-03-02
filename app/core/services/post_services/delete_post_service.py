import asyncio
import uuid
from typing import TYPE_CHECKING

from app.config import MySettings
from app.core.domain.post.exceptions import PostNotFoundError
from app.core.services.post_services.cache_service import user_posts_key
from app.logger import CustomLogger

if TYPE_CHECKING:
    from aiocache import Cache

    from app.core.domain.post.protocols import PostRepositoryInterface


async def detete_post_service(
    user_id: "uuid.UUID",
    post_id: uuid.UUID,
    posts_repo: "PostRepositoryInterface",
    cache: "Cache",
) -> None:
    try:
        await posts_repo.delete_post(
            user_id=user_id,
            post_id=post_id,
        )

        async def delete_cache():
            cache_key = user_posts_key(user_id)
            try:
                vals = await cache.get(cache_key)  # pyright: ignore
                await cache.delete(cache_key)  # pyright: ignore
                new_vals = [val for val in vals if val.id != post_id]
                await cache.set(cache_key, new_vals, ttl=MySettings.CACHE_EXPIRE_MINUTES * 60)  # pyright: ignore
            except Exception:  # noqa: BLE001
                await cache.delete(cache_key)  # pyright: ignore
                CustomLogger.get_logger().error("Error deleting cache", exc_info=True)

        asyncio.create_task(delete_cache())  # noqa: RUF006

    except ValueError as e:
        CustomLogger.get_logger().exception("An error occurred while deleting a post %s", e)
        raise PostNotFoundError() from e
    except Exception as e:
        CustomLogger.get_logger().exception("An error occurred while deleting a post")
        raise Exception() from e
