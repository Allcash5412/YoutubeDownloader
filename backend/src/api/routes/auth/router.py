import logging

from fastapi import APIRouter

from .dependencies import UserRegisterFormDep, UserLoginFormDep
from src.domain.auth.dto import TokenInfo, RegisteredUser
from src.domain.auth.services import LoginService, RegisterService
from src.api.routes.dependencies import UserRepositoryDep

auth = APIRouter(prefix='/auth')
logger = logging.getLogger('app')


@auth.post('/login/', response_model=TokenInfo)
async def auth_user(user_repository: UserRepositoryDep, user_login_form: UserLoginFormDep) -> TokenInfo:
    logger.debug('def auth_user')
    logger.debug(f'user_login_form = {user_login_form}')
    login_service = LoginService(user_repository)
    token = await login_service.login(user_login_form)
    logger.debug(f'token value = {token.dict}')
    return token


@auth.post('/register/', response_model=RegisteredUser)
async def register_user(user_repository: UserRepositoryDep, user_register_form: UserRegisterFormDep) -> RegisteredUser:
    register_service = RegisterService(user_repository)
    registered_user = await register_service.register(user_register_form)
    return registered_user
