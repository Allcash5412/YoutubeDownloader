from typing import Dict

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.domain.auth.schemas import UserBase
from src.domain.auth.dto import UserCreate
from src.repositories.user.interfaces import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by(self, **filter_by) -> UserBase | None:
        query = select(User).filter_by(**filter_by)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return UserBase.from_orm(user) if user else None

    async def update_user_by(self, filter_by: Dict, data_for_update: Dict) -> None:
        await self.session.execute(update(User).filter_by(**filter_by).values(**data_for_update))
        await self.session.commit()

    async def create_user(self, user_to_create: UserCreate) -> UserBase:
        user = User(**user_to_create.model_dump())
        self.session.add(user)
        await self.session.commit()
        return UserBase.from_orm(user)

    async def delete_user(self, filter_by: Dict) -> None:
        await self.session.execute(delete(User).filter_by(**filter_by))
        await self.session.commit()


class TestUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by(self, **filter_by) -> UserBase | None:
        query = select(User).filter_by(**filter_by)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return UserBase.from_orm(user) if user else None

    async def update_user_by(self, filter_by: Dict, data_for_update: Dict) -> None:
        await self.session.execute(update(User).filter_by(**filter_by).values(**data_for_update))

    async def create_user(self, user_to_create: UserCreate) -> UserBase:
        user = User(**user_to_create.model_dump())
        self.session.add(user)
        return UserBase.from_orm(user)

    async def delete_user(self, filter_by: Dict) -> None:
        await self.session.execute(delete(User).filter_by(**filter_by))
