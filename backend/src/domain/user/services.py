from src.domain.user.dto import UserProfile

from src.exceptions import get_exception_404_not_found_with_detail
from src.repositories.user.repositories import AbstractUserRepository


class UserProfileService:

    def __init__(self, repository: AbstractUserRepository):
        """
            Initializes UserProfileService with the given repository.
            :param repository: AbstractUserRepository, repository instance
        """
        self.repository = repository

    async def get_user_profile(self, user_id: int) -> UserProfile:
        user = await self.repository.get_user_by(id=user_id)
        if not user:
            raise get_exception_404_not_found_with_detail('User not found!')
        return UserProfile.from_orm(user)
