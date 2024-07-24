import pytest
from asyncio import current_task
from dataclasses import dataclass
from datetime import datetime

from _pytest.fixtures import FixtureFunction
from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker, create_async_engine

from src.repositories.user.repositories import TestUserRepository
from src.domain.auth.dto import UserCreate
from src.domain.services import PasswordManager
from src.domain.auth.interfaces import AbstractUserRegister
from src.config import settings
from src.utils import random_lower_string, random_email


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@dataclass
class TestUser(AbstractUserRegister):
    username: str
    password: str
    email: str


@dataclass
class TestUserRegister(AbstractUserRegister):
    username: str
    password: str
    email: str


@pytest.fixture(scope='function')
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = create_async_engine(settings.postgres_db.url, echo=True)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope='function')
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return async_scoped_session(async_sessionmaker(bind=db_engine,
                                                   autoflush=True,
                                                   autocommit=False,
                                                   expire_on_commit=False,
                                                   ),
                                scopefunc=current_task)


@pytest.fixture(scope='function')
async def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()

    yield session_

    await session_.rollback()

    await session_.close()


@pytest.fixture
async def user_repository(db_session) -> TestUserRepository:
    return TestUserRepository(db_session)


@pytest.fixture
async def create_user(user_repository: TestUserRepository):
    await user_repository.create_user(UserCreate(username=settings.tests.username,
                                                 password=PasswordManager.hash_password(settings.tests.password),
                                                 email=settings.tests.email,
                                                 register_at=datetime.now()))


@pytest.fixture
async def exist_user(create_user: FixtureFunction):
    yield TestUser(username=settings.tests.username,
                   password=settings.tests.password,
                   email=settings.tests.email)


@pytest.fixture
def non_exist_user():
    user = TestUser(username=random_lower_string(),
                    password=random_lower_string(),
                    email=random_email())
    return user
