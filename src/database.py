from asyncio import current_task

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings

# engine = create_async_engine(DATABASE_URL, echo=True)
# # async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# async_session = async_sessionmaker(engine, expire_on_commit=False)
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

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session


    # async def scoped_session_dependency(self) -> AsyncSession:
    #     session = self.get_scoped_session()
    #     yield session
    #     await session.close()


db_helper = DatabaseHelper(
    url=settings.postgres_db.url,
    echo=False,
)
# Dependency
# async def get_session() -> AsyncGenerator:
#     async with async_session() as session:
#         yield session
