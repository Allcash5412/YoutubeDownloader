from datetime import datetime, UTC, timedelta
from typing import Dict

import bcrypt
import jwt
from jwt import InvalidTokenError

from src.auth.schemas import CredentialsToEncodeToken, CredentialsToDecodeToken
from src.config import settings
from src.exceptions import get_exception_401_unauthorized_with_detail


class CryptJWT:
    @classmethod
    def encode_jwt(cls, token_credentials: CredentialsToEncodeToken):
        to_encode = token_credentials.payload.copy()
        datetime_now = datetime.now(UTC)

        if token_expire_timedelta := token_credentials.expire_timedelta:
            expire = datetime_now + token_expire_timedelta
        else:
            expire = datetime_now + timedelta(minutes=token_credentials.expire_minutes)

        to_encode.update(exp=expire, iat=datetime_now)
        encoded_jwt_token: str = jwt.encode(to_encode, token_credentials.key, algorithm=token_credentials.algorithm)
        return encoded_jwt_token

    @classmethod
    def decode_jwt(cls, token_credentials: CredentialsToDecodeToken) -> Dict:
        try:
            decoded_jwt_token: Dict = jwt.decode(token_credentials.encode_token,
                                                 token_credentials.key,
                                                 algorithms=token_credentials.algorithm)
        except InvalidTokenError:
            raise get_exception_401_unauthorized_with_detail('invalid token error')
        return decoded_jwt_token

    @classmethod
    def get_token_payload(cls, token: str) -> Dict:
        payload = cls.decode_jwt(token)
        return payload


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
