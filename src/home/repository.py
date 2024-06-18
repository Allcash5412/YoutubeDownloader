# from typing import Any
#
# from fastapi import Depends
# from sqlalchemy import Result, select
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.auth.models import User
# from src.database import get_session
#
#
# class UserRepository:
#     def __init__(self, session: AsyncSession = Depends(get_session)):
#         self.session = session
#
#     async def get_user_by_id(self, id: int) -> Result[Any]:
#         return await self.session.execute(select(User).filter(User.id == id))
#
#     async def get_users(self) -> Result[tuple[User]]:
#         return await self.session.execute(select(User))
#
#     def create_user(self, user: User) -> User:
#         self.session.add(user)
#         self.session.commit()
#         return user
#
#     def update_user(self, user: User) -> User:
#         self.session.merge(user)
#         self.session.commit()
#         return user
#
#     def delete_user(self, id: int) -> None:
#         user = self.get_user_by_id(id)
#         self.session.delete(user)
#         self.session.commit()
