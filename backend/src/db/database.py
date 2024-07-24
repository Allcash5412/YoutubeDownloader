from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings

Base = declarative_base()


class DatabaseHelper:
    def __init__(self, url: str, echo):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session
        await self.engine.dispose()

    def get_scoped_session(self):
        return async_scoped_session(self.session_factory, scopefunc=current_task)


db_helper = DatabaseHelper(
    url=settings.postgres_db.url,
    echo=False,
)

