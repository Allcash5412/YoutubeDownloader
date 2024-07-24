import pytest
from fastapi.testclient import TestClient

from tests.conftest import TestUser
from src.main import app

client = TestClient(app)


@pytest.mark.anyio
async def test_get_access_token(exist_user: TestUser) -> None:
    login_data = {
        'username': exist_user.username,
        'password': exist_user.password,
    }
    r = client.post('/auth/login/', data=login_data)
    tokens = r.json()
    assert 'access_token' and 'refresh_token' in tokens
    assert tokens['access_token'] and tokens['refresh_token']
    assert tokens['access_token'] is not None and tokens['refresh_token'] is not None
