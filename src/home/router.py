from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer

from src.auth.schemas import UserAuth, CredentialsToDecodeToken
from src.auth.service import TokenType
from src.exceptions import get_exception_401_unauthorized_with_detail
from src.service import CryptJWT
from src.home.schemas import UserProfileInfo
from src.home.service import UserProfile


http_bearer = HTTPBearer(auto_error=False)
home_page = APIRouter(prefix='/profile', dependencies=[Depends(http_bearer)])
oauth2_scheme = OAuth2PasswordBearer('/auth/login/')


@home_page.get('', response_model=UserProfileInfo)
async def about_user(token: str = Depends(oauth2_scheme)) -> UserProfileInfo:
    # user_info = CryptJWT.get_token_payload(token)
    print(f'token = {token}')
    user_info = CryptJWT.decode_jwt(CredentialsToDecodeToken(token=token))
    token_type = user_info.get('type')
    if token_type != TokenType.ACCESS:
        raise get_exception_401_unauthorized_with_detail('invalid token type!')
    user_profile = UserProfile()
    profile_info = await user_profile.get_profile_info(user_info)
    return profile_info
