import logging

from fastapi import APIRouter

from src.api.routes.dependencies import ValidateToken, UserRepositoryDep
from src.domain.user.services import UserProfileService
from src.domain.user.dto import UserProfile

user = APIRouter(prefix='/user')
logger = logging.getLogger('app')


@user.get('/profile/', response_model=UserProfile)
async def profile(token: ValidateToken, user_repository: UserRepositoryDep) -> UserProfile:
    logger.debug('def profile')
    logger.debug(f'token = {token}')
    user_profile_service = UserProfileService(user_repository)
    user_id = token.sub
    logger.debug(f'user_id = {user_id}')
    user_profile = await user_profile_service.get_user_profile(user_id)
    logger.debug(f'user_profile = {user_profile.dict}')
    return user_profile



