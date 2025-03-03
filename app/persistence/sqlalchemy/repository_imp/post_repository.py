import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.post.entities import PostEntity
from app.core.domain.post.protocols import PostRepositoryInterface
from app.persistence.sqlalchemy.models.post_model import PostTable


class PostRepositoryImp(PostRepositoryInterface[AsyncSession]):
    def __init__(self, *, db_session: AsyncSession):
        self.session = db_session

    async def commit(self) -> None:
        await self.session.commit()

    async def get_all_posts(
        self,
        user_id: uuid.UUID,
    ) -> list[PostEntity]:
        stmt = select(PostEntity).where(PostTable.c.user_id == user_id).order_by(PostTable.c.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add_post(
        self,
        *,
        user_id: uuid.UUID,
        text: str,
        commit: bool = True,
    ) -> PostEntity:
        new_post = PostEntity(user_id=user_id, text=text)
        self.session.add(new_post)
        if commit:
            await self.commit()
        return new_post

    async def delete_post(self, *, user_id: uuid.UUID, post_id: uuid.UUID, commit: bool = True) -> None:
        stmt = delete(PostEntity).where((PostTable.c.id == post_id) & (PostTable.c.user_id == user_id))
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("Post not found")
        if commit:
            await self.commit()


async def get_post_repository(db_session: AsyncSession) -> PostRepositoryInterface:
    return PostRepositoryImp(db_session=db_session)
