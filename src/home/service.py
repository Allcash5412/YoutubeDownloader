from typing import Dict

from src.auth.service import TokenType
from src.exceptions import get_exception_401_unauthorized_with_detail
from src.home.schemas import UserProfileInfo
from src.repository import UserRepository


class UserProfile:
    async def get_profile_info(self, user_info: Dict) -> UserProfileInfo:
        repository = UserRepository()
        user = await repository.get_user_by(username=user_info.get('sub'))
        print(f"user = {user}")
        unauth_exception = get_exception_401_unauthorized_with_detail('user not found')
        if not user:
            raise unauth_exception
        return UserProfileInfo.from_orm(user)
