import uuid
from abc import abstractmethod

from app.core.domain.commons.protocols import AbstractRepository
from app.core.domain.commons.session import SessionType
from app.core.domain.post.entities import PostEntity


class PostRepositoryInterface(AbstractRepository[SessionType]):
    @abstractmethod
    async def get_all_posts(
        self,
        user_id: uuid.UUID,
        limit: int = 10,
        offset: int = 0,
    ) -> list[PostEntity]:
        """Get all posts"""
        ...

    @abstractmethod
    async def add_post(
        self,
        *,
        user_id: uuid.UUID,
        text: str,
        commit: bool = True,
    ) -> PostEntity:
        """Finds a user by their unique identifier (UUID).

        Args:
            user_id (UUID): The unique identifier of the user to find.
            text (str): The text of the post.
            commit (bool): Whether to commit the transaction.

        Returns:
            PostEntity: The post entity.
        """
        ...

    @abstractmethod
    async def delete_post(
        self,
        *,
        user_id: uuid.UUID,
        post_id: uuid.UUID,
        commit: bool = True,
    ) -> None:
        """Finds a user by their email address.

        Args:
            user_id (UUID): The unique identifier of the user.
            post_id (UUID): The unique identifier of the post.
            commit (bool): Whether to commit the transaction.

        Returns:
            None
        """
        ...
