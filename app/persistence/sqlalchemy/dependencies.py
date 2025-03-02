from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.sqlalchemy.connection import async_session_factory


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def get_db_router() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
