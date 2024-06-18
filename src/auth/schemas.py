from datetime import timedelta
from typing import Dict

from pydantic import BaseModel, EmailStr, ConfigDict

from src.config import settings


class UserRead(BaseModel):
    """Other fields in schemas.BaseUser"""
    id: int
    username: str
    email: EmailStr
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Other fields in schemas.BaseUserCreate"""
    username: str
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserAuth(BaseModel):
    """Other fields in schemas.BaseUserCreate"""
    id: int
    username: str
    email: EmailStr
    password: bytes
    model_config = ConfigDict(from_attributes=True)


class TokenInfo(BaseModel):
    access_token: bytes
    refresh_token: bytes
    token_type: str


class CredentialsToEncodeToken(BaseModel):
    payload: Dict
    expire_minutes: int = None
    expire_timedelta: timedelta = None
    key: str = settings.authJWT.key
    algorithm: str = settings.authJWT.algorithm


class CredentialsToDecodeToken(BaseModel):
    encode_token: str
    key: str = settings.authJWT.key
    algorithm: str = settings.authJWT.algorithm


class UserUpdate(BaseModel):
    pass
