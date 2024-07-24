from datetime import datetime

from fastapi import HTTPException

from src.exceptions import get_exception_401_unauthorized_with_detail, get_exception_400_bad_request_with_detail
from src.repositories.user.interfaces import AbstractUserRepository
from src.domain.services import JWTService, PasswordManager

from .interfaces import AbstractUserLogin, AbstractUserRegister
from .schemas import UserBase
from .dto import UserCreate, TokenInfo, RegisteredUser


class RegisterService:
    """ Class provides the ability to create a new user """

    def __init__(self, repository: AbstractUserRepository):
        """
            Initializes RegisterService with the given repository.
            :param repository: AbstractUserRepository, repository instance
        """
        self.repository = repository

    async def register(self, user_register: AbstractUserRegister) -> RegisteredUser:
        """
            Method for registering new users in the system
            :param user_register: AbstractUserRegister, class instance that implements the AbstractUserRegister
            :return: TokenInfo, jwt token for user
        """
        new_user = await self.create_new_user(user_register)
        registered_user = RegisteredUser(**new_user.model_dump())
        return registered_user

    async def create_new_user(self, user_register: AbstractUserRegister) -> UserBase:
        """
            Method for creating new users in db
            :param user_register: AbstractUserRegister, class instance that implements the AbstractUserRegister
            :return: UserBase, created user
        """
        await self.check_on_exiting_user(user_register.username, user_register.email)
        user = self.get_user_create(user_register)
        created_user = await self.repository.create_user(user)
        return created_user

    def get_user_create(self, user_register: AbstractUserRegister) -> UserCreate:
        """
            Method for converting user_register to dto instance UserCreate for further
            convenient saving to db
            :param user_register: AbstractUserRegister, class instance that implements the AbstractUserRegister
            :return: UserCreate, dto instance
        """
        user_data = user_register.__dict__
        user_hashed_password = PasswordManager.hash_password(user_register.password)
        user_data.update(password=user_hashed_password, register_at=datetime.now())
        user = UserCreate(**user_data)
        return user

    async def check_on_exiting_user(self, username: str, email: str) -> bool | HTTPException:
        user_service = UserValidationService(self.repository)
        if await user_service.check_on_exiting_username(username):
            raise get_exception_400_bad_request_with_detail('User with this username already exist!')
        if await user_service.check_on_exiting_email(email):
            raise get_exception_400_bad_request_with_detail('User with this email already exist!')
        return True


class LoginService:
    """ Class provides the ability to auth user """

    def __init__(self, repository: AbstractUserRepository):
        """
            Initializes LoginService with the given repository.
            :param repository: AbstractUserRepository, repository instance
        """
        self.repository = repository

    async def login(self, user_login: AbstractUserLogin) -> TokenInfo:
        """
            Method for login users in the system
            :param user_login: AbstractUserLogin, class instance that implements the AbstractUserLogin
            :return: TokenInfo, jwt token for user
        """
        user = await self.get_user(user_login)
        await self.repository.update_user_by({'id': user.id},
                                             {'last_login': datetime.now()})
        token = JWTService.get_jwt(user)
        return token

    async def get_user(self, user_login: AbstractUserLogin) -> UserBase:
        """
            Method for obtain a user from the database
            :param user_login: AbstractUserLogin, class instance that implements the AbstractUserLogin
            :return: UserBase, user entity
        """
        user_service = UserValidationService(self.repository)
        user = await self.repository.get_user_by(username=user_login.username)
        user_service.check_user_credentials(user, user_login.password)
        return user


class UserValidationService:
    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    async def check_on_exiting_user(self, username: str, email: str) -> bool:
        return await self.check_on_exiting_username(username) and await self.check_on_exiting_email(email)

    async def check_on_exiting_username(self, username: str) -> bool:
        if await self.repository.get_user_by(username=username):
            return True
        return False

    async def check_on_exiting_email(self, email: str) -> bool:
        if await self.repository.get_user_by(email=email):
            return True
        return False

    def check_user_credentials(self, user: UserBase, received_password: str) -> bool | HTTPException:
        if not user or not PasswordManager.validate_password(received_password, user.password.encode()):
            raise get_exception_401_unauthorized_with_detail('invalid username or password')
        return True
