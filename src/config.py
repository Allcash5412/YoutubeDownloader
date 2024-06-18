from pathlib import Path

from pydantic import Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = 'src'

MODEL_FILE_NAME = 'models.py'

# add all your app modules here.
INSTALLED_APPS = [
   'src.auth'
]

default_config = SettingsConfigDict(env_file=BASE_DIR / 'src' / '.env', extra='ignore')


class PostgresSettings(BaseSettings):
    model_config = default_config
    user: str = Field(alias='DB_USER')
    password: str = Field(alias='DB_PASS')
    host: str = Field(alias='DB_HOST')
    port: int = Field(alias='DB_PORT')
    db_name: str = Field(alias='DB_NAME')
    url: str = ''

    @field_validator('url')
    def get_database_url(cls, v, info: FieldValidationInfo):
        data = info.data
        return f'postgresql+asyncpg://{data['user']}:{data['password']}@{data['host']}:{data['port']}/{data['db_name']}'


class AuthJWT(BaseSettings):
    model_config = default_config
    key: str = Field('SECRET')
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    postgres_db: PostgresSettings = PostgresSettings()
    authJWT: AuthJWT = AuthJWT()


settings = Settings()
