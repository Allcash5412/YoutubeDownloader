from enum import Enum

import bcrypt
import jwt
from fastapi import HTTPException
from jwt import InvalidTokenError

from datetime import datetime, UTC, timedelta

from src.domain.auth.schemas import UserBase
from src.domain.auth.dto import TokenInfo, TokenPayload, CredentialsToEncodeToken, CredentialsToDecodeToken

from src.config import settings
from src.exceptions import get_exception_401_unauthorized_with_detail


class TokenType(Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class JWTService:
    @staticmethod
    def encode_jwt(token_credentials: CredentialsToEncodeToken) -> str:
        payload = token_credentials.payload.copy()
        datetime_now = datetime.now(UTC)

        if token_expire_timedelta := token_credentials.expire_timedelta:
            expire = datetime_now + token_expire_timedelta
        else:
            expire = datetime_now + timedelta(minutes=token_credentials.expire_minutes)

        payload.exp = expire
        payload.iat = datetime_now

        encoded_jwt_token = jwt.encode(payload.model_dump(), token_credentials.key,
                                       algorithm=token_credentials.algorithm)
        return encoded_jwt_token

    @staticmethod
    def decode_jwt(token_credentials: CredentialsToDecodeToken) -> TokenPayload:
        try:
            decoded_jwt_token = jwt.decode(token_credentials.encode_token,
                                           token_credentials.key,
                                           algorithms=token_credentials.algorithm)
        except InvalidTokenError:
            raise get_exception_401_unauthorized_with_detail('invalid token error')
        return TokenPayload(**decoded_jwt_token)

    @staticmethod
    def check_token_type(token_type: str) -> None | HTTPException:
        if token_type != TokenType.ACCESS.value:
            raise get_exception_401_unauthorized_with_detail('invalid token type!')
        return None

    @classmethod
    def _get_token_payload(cls, user_id: int, token_type: TokenType) -> TokenPayload:
        token_payload = TokenPayload(sub=user_id, type=token_type.value)
        return token_payload

    @classmethod
    def _get_access_token(cls, user: UserBase) -> str:
        access_token_payload = cls._get_token_payload(user.id, TokenType.ACCESS)

        token_credentials = CredentialsToEncodeToken(payload=access_token_payload,
                                                     expire_minutes=settings.authJWT.access_token_expire_minutes,
                                                     )
        access_token = cls.encode_jwt(token_credentials)
        return access_token

    @classmethod
    def _get_refresh_token(cls, user: UserBase):
        refresh_token_payload = cls._get_token_payload(user.id, TokenType.REFRESH)
        token_credentials = CredentialsToEncodeToken(payload=refresh_token_payload,
                                                     key=settings.authJWT.key,
                                                     expire_timedelta=timedelta(
                                                         days=settings.authJWT.refresh_token_expire_days),
                                                     )
        refresh_token = cls.encode_jwt(token_credentials)
        return refresh_token

    @staticmethod
    def get_jwt(user: UserBase) -> TokenInfo:
        access_token = JWTService._get_access_token(user)
        refresh_token = JWTService._get_refresh_token(user)
        token_type = settings.authJWT.token_type
        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type)


class PasswordManager:

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        password_bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)

    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password)
