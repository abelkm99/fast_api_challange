import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.core.domain.post.entities import PostEntity


class PostBase(BaseModel):
    text: str


class PostSchema(BaseModel):
    id: uuid.UUID


class PostOutSchema(PostSchema, PostBase):
    id: uuid.UUID

    @staticmethod
    def from_entity(post_entity: "PostEntity") -> "PostOutSchema":
        return PostOutSchema(
            id=post_entity.id,
            text=post_entity.text,
        )
