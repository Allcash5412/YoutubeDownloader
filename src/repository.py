from typing import Any, Dict

from fastapi import Depends, HTTPException
from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from src.auth.models import User
from src.auth.schemas import UserRead, UserAuth
from src.database import db_helper


# class UnitOfWork():
#     def __init__(self) -> None:
#         self._session_maker = async_session
#
#     async def __aenter__(self) -> AbstractUnitOfWork:
#         self._session = self._session_maker()
#         self.repository1 = Repository1(self._session)
#         self.repository2 = Repository2(self._session)
#         return self
#
#     async def __aexit__(self, *args) -> None:
#         await self._session.rollback()
#         await self._session.close()
#
#     async def commit(self) -> None:
#         await self._session.commit()

class UserRepository:
    def __init__(self):
        self.session = db_helper.session_factory

    # async def get_session(self):
    #     return await anext(get_session())

    async def get_user_by(self, **filter_by) -> User:
        async with self.session() as session:
            async with session.begin():
                query = select(User).filter_by(**filter_by)
                result = await session.execute(query)
                print(f"result = {result}")
                user = result.scalars().first()
                print(f'get_user_by user = {user}')
                if user is None:
                    raise HTTPException(status_code=404, detail="User not found")

                return user

    async def get_users(self) -> Result[tuple[User]]:
        return await self.session.execute(select(User))

    async def update_user_by(self, filter_by: Dict, data_for_update: Dict) -> None:
        async with self.session() as session:
            async with session.begin():
                await session.execute(update(User).filter_by(**filter_by).values(**data_for_update))
                await session.commit()

    def create_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        return user



    def delete_user(self, id: int) -> None:
        user = self.get_user_by_id(id)
        self.session.delete(user)
        self.session.commit()

# async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
#     return UserRepository(session)
