from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Form
from pydantic import EmailStr, BaseModel

from src.domain.auth.interfaces import AbstractUserLogin, AbstractUserRegister
from src.config import settings


@dataclass
class UserLoginForm(AbstractUserLogin):
    username: Annotated[str, Form()]
    password: Annotated[str, Form()]


@dataclass
class UserRegisterForm(UserLoginForm, AbstractUserRegister):
    email: Annotated[EmailStr, Form()]


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    register_at: datetime | None


class TokenInfo(BaseModel):
    access_token: bytes
    refresh_token: bytes
    token_type: str


class TokenPayload(BaseModel):
    sub: int
    type: str
    exp: datetime | None = None
    iat: datetime | None = None


class CredentialsToEncodeToken(BaseModel):
    payload: TokenPayload
    expire_minutes: int = None
    expire_timedelta: timedelta = None
    key: str = settings.authJWT.key
    algorithm: str = settings.authJWT.algorithm


class CredentialsToDecodeToken(BaseModel):
    encode_token: str
    key: str = settings.authJWT.key
    algorithm: str = settings.authJWT.algorithm


class RegisteredUser(BaseModel):
    username: str
    email: EmailStr
