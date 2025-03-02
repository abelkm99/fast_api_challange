import uuid

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.commons.schemas import MetaData, Paginate
from app.core.domain.user.entities import (
    UserEntity,
)
from app.core.domain.user.protocols import UserRepositoryInterface
from app.persistence.sqlalchemy.models.user_model import (
    UserTable,
)


class UserRepositoryImp(UserRepositoryInterface[AsyncSession]):
    def __init__(self, *, db_session: AsyncSession):
        self.session = db_session

    async def commit(self) -> None:
        await self.session.commit()

    async def get_all_users(self, limit: int = 10, offset: int = 0) -> Paginate[UserEntity]:
        # Select all users ordered by creation date (assuming created_at exists on your BaseEntity)
        stmt = select(UserEntity).order_by(UserTable.c.created_at.desc()).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        users = list(result.scalars().all())

        # Get total count
        count_stmt = select(func.count()).select_from(UserTable)
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar() or 0

        meta_data = MetaData(total=total, offset=offset, limit=limit, returned=len(users))
        return Paginate(items=users, meta_data=meta_data)

    async def find_by_id(self, *, user_id: uuid.UUID) -> UserEntity | None:
        stmt = select(UserEntity).where(UserTable.c.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_email(self, *, email_address: str) -> UserEntity | None:
        stmt = select(UserEntity).where(func.lower(UserTable.c.email_address) == func.lower(email_address))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_new_user(self, *, email_address: str, password: str, commit: bool = True) -> UserEntity:
        new_user = UserEntity(
            email_address=email_address,
            password=password,
            is_archived=False,
            is_activated=False,
        )
        self.session.add(new_user)
        if commit:
            await self.commit()
        return new_user

    async def delete_user(self, *, user_id: uuid.UUID, commit: bool = True) -> None:
        stmt = delete(UserEntity).where(UserTable.c.id == user_id)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("User not found")
        if commit:
            await self.commit()

    async def change_password(self, *, user_id: uuid.UUID, new_password: str, commit: bool = True) -> None:
        stmt = update(UserEntity).where(UserTable.c.id == user_id).values(password=new_password)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("User not found")
        if commit:
            await self.commit()


async def get_user_repository(db_session: AsyncSession) -> UserRepositoryInterface:
    return UserRepositoryImp(
        db_session=db_session,
    )
