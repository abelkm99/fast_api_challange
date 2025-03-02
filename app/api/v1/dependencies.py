import uuid
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.guards import oauth2_scheme
from app.core.domain.user.exceptions import InvalidTokenError, UserNotFoundError
from app.core.services.authentication_services.utils import decode_token
from app.persistence.cache import get_in_memory_cache
from app.persistence.sqlalchemy.dependencies import get_db_router
from app.persistence.sqlalchemy.repository_imp.post_repository import get_post_repository
from app.persistence.sqlalchemy.repository_imp.user_repository import get_user_repository

if TYPE_CHECKING:
    from app.core.domain.commons.session import SessionType
    from app.core.domain.user.entities import UserEntity
    from app.core.domain.user.protocols import UserRepositoryInterface


async def user_repo_dependency(
    db_session: Annotated[AsyncSession, Depends(get_db_router)],
):
    return await get_user_repository(db_session)


async def posts_repo_dependency(
    db_session: Annotated[AsyncSession, Depends(get_db_router)],
):
    return await get_post_repository(db_session)


def get_cache_dependency():
    return get_in_memory_cache()


async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> "uuid.UUID":
    payload = decode_token(token)
    if "sub" not in payload:
        raise InvalidTokenError()
    return uuid.UUID(payload["sub"])


async def get_current_user_entity(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    user_repo: Annotated["UserRepositoryInterface[SessionType]", Depends(user_repo_dependency)],
) -> "UserEntity":
    user = await user_repo.find_by_id(user_id=user_id)
    if not user:
        raise UserNotFoundError()
    return user
