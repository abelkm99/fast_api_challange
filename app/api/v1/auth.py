from typing import Annotated

from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm

import app.core.services.authentication_services as auth_service
from app.api.v1.dependencies import user_repo_dependency
from app.core.domain.commons.session import SessionType
from app.core.domain.user.protocols import UserRepositoryInterface
from app.core.services.authentication_services.schemas import (
    AuthenticatedUser,
    SignUpSchema,
    UserOutSchema,
)

authentication_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@authentication_router.post("/sign_in", response_model=AuthenticatedUser)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: Annotated["UserRepositoryInterface[SessionType]", Depends(user_repo_dependency)],
) -> AuthenticatedUser:
    return await auth_service.sign_in_service(
        username=form_data.username,
        password=form_data.password,
        user_repository=user_repo,
    )


@authentication_router.post(
    "/sign_up",
    response_model=UserOutSchema,
)
async def sign_up(
    data: SignUpSchema,
    user_repo: Annotated["UserRepositoryInterface[SessionType]", Depends(user_repo_dependency)],
) -> UserOutSchema:
    return await auth_service.sign_up_service(
        data=data,
        user_repository=user_repo,
    )


@authentication_router.get(
    "/refresh_token",
    description="to refresh the access token, user will send the refresh token and receive a new access token",
)
async def refresh_token(
    refresh_token: Annotated[str, Header(...)],
    user_repo: Annotated[UserRepositoryInterface[SessionType], Depends(user_repo_dependency)],
) -> dict[str, str]:
    return await auth_service.generate_access_token_service(
        refresh_token=refresh_token,
        user_repository=user_repo,
    )
