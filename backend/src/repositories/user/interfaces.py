from abc import ABC, abstractmethod
from typing import Dict

from src.domain.auth.schemas import UserBase
from src.domain.auth.dto import UserCreate


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_user_by(self, **filter_by) -> UserBase:
        pass

    @abstractmethod
    def update_user_by(self, filter_by: Dict, data_for_update: Dict):
        pass

    @abstractmethod
    def create_user(self, user: UserCreate) -> UserBase:
        pass

    @abstractmethod
    def delete_user(self, filter_by: Dict) -> None:
        pass
