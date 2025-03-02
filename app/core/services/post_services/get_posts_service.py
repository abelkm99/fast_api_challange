from typing import TYPE_CHECKING

from app.core.services.post_services.schemas import PostOutSchema

if TYPE_CHECKING:
    from app.core.domain.post.protocols import PostRepositoryInterface
    from app.core.domain.user.entities import UserEntity


async def get_posts_service(
    user: "UserEntity",
    posts_repo: "PostRepositoryInterface",
) -> "list[PostOutSchema]":
    res = await posts_repo.get_all_posts(
        user_id=user.id,
    )
    return [PostOutSchema.from_entity(post) for post in res]
