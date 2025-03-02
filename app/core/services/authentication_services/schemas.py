import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr

if TYPE_CHECKING:
    from app.core.domain.user.entities import UserEntity


class UserBaseSchema(BaseModel):
    email_address: EmailStr


class PasswordSchema(BaseModel):
    password: str
    confirm_password: str


class SignUpSchema(PasswordSchema, UserBaseSchema): ...


class SignInSchema(BaseModel):
    email_address: str
    password: str


class UserOutSchema(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_user_entity(user_entity: "UserEntity") -> "UserOutSchema":
        return UserOutSchema(
            id=user_entity.id,
            email_address=user_entity.email_address,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at,
        )


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class AuthenticatedUser(UserOutSchema, TokenSchema):
    @staticmethod
    def from_user_entity(  # type: ignore
        user_entity: "UserEntity",
        access_token: str,
        refresh_token: str,
        token_type: str = "bearer",  # noqa: S107
    ) -> "AuthenticatedUser":
        return AuthenticatedUser(
            id=user_entity.id,
            email_address=user_entity.email_address,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
        )
