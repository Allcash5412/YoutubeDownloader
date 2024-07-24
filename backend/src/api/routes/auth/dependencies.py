from typing import Annotated

from fastapi import Depends

from src.domain.auth.interfaces import AbstractUserLogin, AbstractUserRegister
from src.domain.auth.dto import UserLoginForm, UserRegisterForm

UserLoginFormDep = Annotated[AbstractUserLogin, Depends(UserLoginForm)]
UserRegisterFormDep = Annotated[AbstractUserRegister, Depends(UserRegisterForm)]
