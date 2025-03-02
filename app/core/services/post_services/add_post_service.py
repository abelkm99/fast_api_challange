import sys
from typing import TYPE_CHECKING

from app.config import MySettings
from app.core.domain.post.exceptions import PostPayloadTooLargeError
from app.core.services.post_services.schemas import PostSchema
from app.logger import CustomLogger

if TYPE_CHECKING:
    from app.core.domain.post.protocols import PostRepositoryInterface
    from app.core.domain.user.entities import UserEntity


async def add_post_service(
    user: "UserEntity",
    text: str,
    posts_repo: "PostRepositoryInterface",
) -> "PostSchema":
    size_mb = sys.getsizeof(text) / 1024 / 1024

    if size_mb > MySettings.TEXT_SIZE_LIMIT_MB:
        raise PostPayloadTooLargeError(
            message=f"Post payload exceeds the maximum allowed size {MySettings.TEXT_SIZE_LIMIT_MB} MB"
        )
    try:
        res = await posts_repo.add_post(
            user_id=user.id,
            text=text,
        )

        return PostSchema(id=res)
    except Exception as e:
        CustomLogger.get_logger().exception("An error occurred while adding a post")
        raise e
