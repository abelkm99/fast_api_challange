import uuid
from typing import TYPE_CHECKING

from app.core.domain.post.exceptions import PostNotFoundError
from app.logger import CustomLogger

if TYPE_CHECKING:
    from app.core.domain.post.protocols import PostRepositoryInterface
    from app.core.domain.user.entities import UserEntity


async def detete_post_service(
    user: "UserEntity",
    post_id: uuid.UUID,
    posts_repo: "PostRepositoryInterface",
) -> None:
    try:
        await posts_repo.delete_post(
            user_id=user.id,
            post_id=post_id,
        )
    except ValueError as e:
        CustomLogger.get_logger().exception("An error occurred while deleting a post %s", e)
        raise PostNotFoundError() from e
    except Exception as e:
        CustomLogger.get_logger().exception("An error occurred while deleting a post")
        raise Exception() from e
