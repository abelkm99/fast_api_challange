from dataclasses import dataclass

from pydantic import EmailStr

from app.core.domain.commons.entities.base_entity import BaseEntity


@dataclass(kw_only=True)
class UserEntity(BaseEntity):
    email_address: EmailStr
    password: str
    is_archived: bool = False
    is_activated: bool = False
