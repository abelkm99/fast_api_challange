import datetime

from app.config import MySettings
from app.core.domain.commons.session import SessionType
from app.core.domain.user.exceptions import (
    IncorrectPasswordError,
    InvalidTokenError,
    UserNotFoundError,
)
from app.core.domain.user.protocols import UserRepositoryInterface
from app.core.services.authentication_services.schemas import AuthenticatedUser
from app.core.services.authentication_services.utils import decode_token, generate_new_token


async def sign_in_service(
    username: str,
    password: str,
    user_repository: UserRepositoryInterface[SessionType],
):
    db_user = await user_repository.find_by_email(
        email_address=username,
    )
    if not db_user:
        raise UserNotFoundError()

    if db_user.password != password:
        raise IncorrectPasswordError()

    access_token = generate_new_token(
        data={"sub": db_user.id.hex},
        expires_delta=datetime.timedelta(minutes=MySettings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = generate_new_token(
        data={"sub": db_user.id.hex},
        expires_delta=datetime.timedelta(days=MySettings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    return AuthenticatedUser.from_user_entity(
        user_entity=db_user,
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def generate_access_token_service(
    refresh_token: str,
    user_repository: UserRepositoryInterface[SessionType],
) -> dict[str, str]:
    payload = decode_token(refresh_token)

    if "sub" not in payload:
        raise InvalidTokenError()

    user = await user_repository.find_by_id(user_id=payload["sub"])
    if not user:
        raise UserNotFoundError()

    access_token = generate_new_token(
        data={"sub": user.id.hex},
        expires_delta=datetime.timedelta(minutes=MySettings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token}
