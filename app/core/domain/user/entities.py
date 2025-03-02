from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pydantic import EmailStr

from app.core.domain.commons.entities.base_entity import BaseEntity

if TYPE_CHECKING:
    from app.core.domain.post.entities import PostEntity


@dataclass(kw_only=True)
class UserEntity(BaseEntity):
    email_address: EmailStr
    password: str
    posts: list["PostEntity"] = field(
        default_factory=list,
        repr=False,
    )
    is_archived: bool = False
    is_activated: bool = False
