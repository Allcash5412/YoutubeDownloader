import pytest

from tests.conftest import TestUser

from src.domain.auth.services import UserValidationService

from src.repositories.user.repositories import UserRepository


class TestUser:
    @pytest.mark.anyio
    async def test_check_on_exiting_user(self, user_repository: UserRepository,
                                         exist_user: TestUser,
                                         non_exist_user: TestUser) -> None:
        user_service = UserValidationService(user_repository)
        check_with_exist_user = await user_service.check_on_exiting_user(exist_user.username,
                                                                         exist_user.email)
        assert check_with_exist_user is True

        check_with_non_exist_user = await user_service.check_on_exiting_user(non_exist_user.username,
                                                                             non_exist_user.password)
        assert check_with_non_exist_user is False

    @pytest.mark.anyio
    async def test_check_on_exiting_username(self, user_repository: UserRepository,
                                             exist_user: TestUser,
                                             non_exist_user: TestUser
                                             ) -> None:
        user_service = UserValidationService(user_repository)
        check_with_exist_username = await user_service.check_on_exiting_username(exist_user.username)
        assert check_with_exist_username is True

        check_with_non_exist_username = await user_service.check_on_exiting_username(non_exist_user.username)
        assert check_with_non_exist_username is False

    @pytest.mark.anyio
    async def test_check_on_exiting_email(self, user_repository: UserRepository,
                                          exist_user: TestUser,
                                          non_exist_user: TestUser) -> None:
        user_service = UserValidationService(user_repository)
        check_with_exist_email = await user_service.check_on_exiting_email(exist_user.email)
        assert check_with_exist_email is True

        check_with_non_exist_email = await user_service.check_on_exiting_email(non_exist_user.email)
        assert check_with_non_exist_email is False
