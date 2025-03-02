import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.core.domain.commons.entities.base_entity import BaseEntity

if TYPE_CHECKING:
    from app.core.domain.user.entities import UserEntity


@dataclass(kw_only=True)
class PostEntity(BaseEntity):
    user_id: uuid.UUID
    text: str
    user: "UserEntity | None" = field(
        init=False,
        default=None,
    )
