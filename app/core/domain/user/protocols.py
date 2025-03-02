import uuid
from abc import abstractmethod

from app.core.domain.commons.protocols import AbstractRepository
from app.core.domain.commons.schemas import Paginate
from app.core.domain.commons.session import SessionType
from app.core.domain.user.entities import UserEntity


class UserRepositoryInterface(AbstractRepository[SessionType]):
    @abstractmethod
    async def get_all_users(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> Paginate[UserEntity]:
        """Get all users"""
        ...

    @abstractmethod
    async def find_by_id(self, *, user_id: uuid.UUID) -> UserEntity | None:
        """Finds a user by their unique identifier (UUID).

        Args:
            user_id (UUID): The unique identifier of the user to find.

        Returns:
            Optional[UserEntity]: The user object if found, None otherwise.
        """
        ...

    @abstractmethod
    async def find_by_email(
        self,
        *,
        email_address: str,
    ) -> UserEntity | None:
        """Finds a user by their email address.

        Args:
            email_address (str): The email address of the user to find.

        Returns:
            Optional[UserEntity]: The user object if found, None otherwise.
        """
        ...

    @abstractmethod
    async def add_new_user(
        self,
        *,
        email_address: str,
        password: str,
        commit: bool = True,
    ) -> UserEntity:
        """Creates a new user in the database.

        Args:
            email_address (str): The email address of the user.
            phone_number (str): The phone number of the user.
            password (str): The password of the user.
            commit (bool): Whether to commit the transaction or not.

        Returns:
            UserEntity: The created user object.
        """

    @abstractmethod
    async def delete_user(self, *, user_id: uuid.UUID, commit: bool = True) -> None:
        """Deletes a user and all related data in the database.

        Args:
            user_id (UUID): The unique identifiers of the user to delete.
            commit (bool): Whether to commit the transaction or not.
        """
        ...

    @abstractmethod
    async def change_password(self, *, user_id: uuid.UUID, new_password: str, commit: bool = True) -> None:
        """Update password
        Args:
            user_id (uuid.UUID)
            new_password (str)
            commit (bool)

        Returns:
            None
        """
        ...
