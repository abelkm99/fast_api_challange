from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession


class FakeDBSession:
    async def execute(self): ...
    async def flush(self): ...
    async def commit(self): ...
    async def rollback(self): ...


SessionType = TypeVar("SessionType", bound=AsyncSession | FakeDBSession)
