from abc import abstractmethod
from typing import Generic, Protocol, runtime_checkable

from app.core.domain.commons.protocols import AbstractRepository
from app.core.domain.commons.session import SessionType


@runtime_checkable
class AbstractUnitOfWork(Protocol, Generic[SessionType]):
    repositories: dict[str, AbstractRepository[SessionType]] = {}
    session: SessionType

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            await self.rollback()
            raise exc_value
        await self.commit()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    def add_repository(self, name: str, repository: AbstractRepository):
        self.repositories[name] = repository

    def get_repository(self, name: str) -> AbstractRepository | None:
        return self.repositories.get(name)
