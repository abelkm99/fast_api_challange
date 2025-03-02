from typing import TYPE_CHECKING

from app.core.services.authentication_services.schemas import SignUpSchema, UserOutSchema

if TYPE_CHECKING:
    from app.core.domain.user.protocols import UserRepositoryInterface


async def sign_up_service(
    data: SignUpSchema,
    user_repository: "UserRepositoryInterface",
):
    if data.password != data.confirm_password:
        raise ValueError("Incorrect confirm password")

    user_entity = await user_repository.add_new_user(
        email_address=data.email_address,
        password=data.password,
    )

    return UserOutSchema.from_user_entity(user_entity)
