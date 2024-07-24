from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.auth.dto import CredentialsToDecodeToken, TokenPayload
from src.domain.services import JWTService

from src.db.database import db_helper
from src.repositories.user.repositories import UserRepository


SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]
oauth2_scheme = OAuth2PasswordBearer('/auth/login/')
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


async def validate_token(token: TokenDep) -> TokenPayload | HTTPException:
    token_payload = JWTService.decode_jwt(CredentialsToDecodeToken(encode_token=token))
    JWTService.check_token_type(token_payload.type)
    return token_payload


ValidateToken = Annotated[TokenPayload, Depends(validate_token)]
