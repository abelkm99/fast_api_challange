from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import uuid


def user_posts_key(user_id: "uuid.UUID") -> str:
    return f"user_posts:user:{user_id}"
