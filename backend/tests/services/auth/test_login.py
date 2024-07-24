import pytest

from fastapi import HTTPException

from tests.conftest import TestUser
from src.domain.services import PasswordManager
from src.repositories.user.interfaces import AbstractUserRepository
from src.domain.auth.schemas import UserBase
from src.domain.auth.dto import TokenInfo
from src.domain.auth.services import LoginService

from src.exceptions import get_exception_401_unauthorized_with_detail


class TestLogin:

    @pytest.mark.anyio
    async def test_login(self, user_repository: AbstractUserRepository, exist_user: TestUser,
                         non_exist_user: TestUser) -> None:

        login_service = LoginService(user_repository)
        token = await login_service.login(exist_user)

        assert type(token) is TokenInfo
        assert (token.access_token and token.refresh_token) is not None

        with pytest.raises(HTTPException):
            await login_service.login(non_exist_user)
            assert get_exception_401_unauthorized_with_detail

    @pytest.mark.anyio
    async def test_get_user(self, user_repository: AbstractUserRepository, exist_user: TestUser,
                            non_exist_user: TestUser) -> None:
        login_service = LoginService(user_repository)
        user = await login_service.get_user(exist_user)

        assert type(user) is UserBase
        assert (user.username == exist_user.username and
                PasswordManager.validate_password(exist_user.password,
                                                  user.password.encode()))

        with pytest.raises(HTTPException):
            await login_service.get_user(non_exist_user)
            assert get_exception_401_unauthorized_with_detail

