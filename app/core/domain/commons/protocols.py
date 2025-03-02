from typing import Generic, Protocol, runtime_checkable

from app.core.domain.commons.session import SessionType


@runtime_checkable
class AbstractRepository(Protocol, Generic[SessionType]):
    session: SessionType

    async def flush(self):
        await self.session.flush()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
