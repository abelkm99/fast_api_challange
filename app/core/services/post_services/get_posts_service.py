from typing import TYPE_CHECKING

from app.core.services.post_services.schemas import PostOutSchema

if TYPE_CHECKING:
    import uuid

    from app.core.domain.post.protocols import PostRepositoryInterface


async def get_posts_service(
    user_id: "uuid.UUID",
    posts_repo: "PostRepositoryInterface",
) -> "list[PostOutSchema]":
    res = await posts_repo.get_all_posts(
        user_id=user_id,
    )
    return [PostOutSchema.from_entity(post) for post in res]
