from fastapi import APIRouter, Form

from src.auth.schemas import TokenInfo
from src.auth.service import Auth


auth = APIRouter(prefix='/auth')


@auth.post('/login/', response_model=TokenInfo)
async def auth_user(username: str = Form(), password: str = Form()):
    auth = Auth()
    user = await auth.auth_user(username, password)
    token = auth.get_jwt(user)
    return token
    # return token
    # jwt_payload = {
    #     'sub': user.username,
    #     'username': user.username,
    #     'email': user.email
    # }
    # token = CryptJWT.encode_jwt(jwt_payload,
    #                             AuthJWT.private_key_jwt,
    #                             AuthJWT.access_token_expire_minutes)
    # return TokenInfo(
    #     access_token=token,
    #     token_type='Bearer')
