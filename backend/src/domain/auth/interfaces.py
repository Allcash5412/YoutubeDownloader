from pydantic import EmailStr
from abc import ABC


class AbstractUserLogin(ABC):
    username: str
    password: str


class AbstractUserRegister(AbstractUserLogin):
    email: EmailStr
