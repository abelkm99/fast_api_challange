from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import MySettings

async_engine = create_async_engine(
    url=MySettings.DATABASE_URL,
    future=True,
    pool_size=20,
    max_overflow=20,
)

async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    async_engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)
