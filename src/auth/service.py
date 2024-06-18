from datetime import datetime, timedelta
from enum import Enum
from typing import Dict

from src.auth.schemas import UserAuth, TokenInfo, CredentialsToEncodeToken
from src.config import settings
from src.exceptions import get_exception_401_unauthorized_with_detail
from src.repository import UserRepository
from src.service import validate_password, CryptJWT


class TokenType(Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class Auth:

    async def auth_user(self, username: str, password: str) -> UserAuth:
        repository = UserRepository()
        user = await repository.get_user_by(username=username)
        await repository.update_user_by({'id': user.id},
                                        {'last_login': datetime.now()})
        if not user or not validate_password(password, user.password.encode()):
            raise get_exception_401_unauthorized_with_detail('invalid username or password')
        return UserAuth.from_orm(user)

    def _get_token_payload(self, user_id: int, token_type: TokenType) -> Dict:
        access_token_payload = {'sub': user_id, 'type': token_type.value}
        return access_token_payload

    def _get_access_token(self, user: UserAuth) -> str:
        access_token_payload = self._get_token_payload(user.id, TokenType.ACCESS)

        token_credentials = CredentialsToEncodeToken(payload=access_token_payload,
                                                     key=settings.authJWT.key,
                                                     expire_minutes=settings.authJWT.access_token_expire_minutes,
                                                     )
        access_token = CryptJWT.encode_jwt(token_credentials)
        return access_token

    def _get_refresh_token(self, user: UserAuth):
        refresh_token_payload = self._get_token_payload(user.id, TokenType.REFRESH)
        token_credentials = CredentialsToEncodeToken(payload=refresh_token_payload,
                                                     key=settings.authJWT.key,
                                                     expire_timedelta=timedelta(days=settings.authJWT.refresh_token_expire_days),
                                                     )
        refresh_token = CryptJWT.encode_jwt(token_credentials)
        return refresh_token

    def get_jwt(self, user: UserAuth):
        access_token = self._get_access_token(user)
        refresh_token = self._get_refresh_token(user)
        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='Bearer')
