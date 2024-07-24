from pathlib import Path
from typing import Dict

from pydantic import Field, field_validator, AnyUrl
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging.config

BASE_DIR = Path(__file__).resolve().parent.parent
default_config = SettingsConfigDict(env_file=BASE_DIR / 'src' / '.env', extra='ignore')


class GlobalSettings(BaseSettings):
    model_config = default_config
    start_settings: str = Field(alias='START_SETTING')
    backend_cors_origins: [AnyUrl] = Field(alias='BACKEND_CORS_ORIGINS')
    logger_config: Dict = {}

    @field_validator('logger_config')
    def get_logger_config(cls, v, info: FieldValidationInfo):
        data = info.data
        logger_config = cls.get_logger_config_by_setting(data['start_settings'])
        return logger_config

    @classmethod
    def get_logger_config_by_setting(cls, start_settings: str) -> Dict:
        if start_settings == 'PRODUCTION':
            LOGGER_CONFIG = {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "simple": {
                        "format": "%(levelname)s: %(message)s"
                    },
                    "detailed": {
                        "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
                        "datefmt": "%Y-%m-%dT%H:%M:%S%z"
                    }
                },
                "handlers": {
                    'console': {
                        'level': 'WARNING',
                        'class': 'logging.StreamHandler',
                        'formatter': 'verbose'
                    },
                    'file': {
                        'level': 'INFO',
                        'class': 'logging.handlers.TimedRotatingFileHandler',
                        'filename': 'app.log',
                        'when': 'W0',
                        'utc': True,
                        'formatter': 'verbose',
                    },
                },
                "loggers": {
                    "root": {
                        # "level": "INFO",
                        "handlers": [
                            "console",
                            # "file"
                        ]
                    }
                }
            }
        else:
            LOGGER_CONFIG = {
                "version": 1,
                "disable_existing_loggers": True,
                "formatters": {
                    "detailed": {
                        "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
                        "datefmt": "%Y-%m-%dT%H:%M:%S%z"
                    }
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "DEBUG",
                        "formatter": "detailed",
                        "stream": "ext://sys.stderr"
                    },
                    # "file": {
                    #     "class": "logging.handlers.RotatingFileHandler",
                    #     "level": "WARNING",
                    #     "formatter": "detailed",
                    #     "filename": "logs/my_app.log",
                    #     "maxBytes": 10000,
                    #     "backupCount": 3
                    # }
                },
                "loggers": {
                    "app": {
                        "level": "DEBUG",
                        "handlers": [
                            "console",
                            # "file"
                        ]
                    }
                }
            }

        return LOGGER_CONFIG


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
    key: str = Field(alias='SECRET')
    algorithm: str = 'HS256'
    token_type: str = 'Bearer'
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class ForTesting(BaseSettings):
    model_config = default_config
    username: str = Field(alias='TEST_USERNAME')
    password: str = Field(alias='TEST_PASSWORD')
    email: str = Field(alias='TEST_EMAIL')


class Settings(BaseSettings):
    postgres_db: PostgresSettings = PostgresSettings()
    authJWT: AuthJWT = AuthJWT()
    tests: ForTesting = ForTesting()
    global_settings: GlobalSettings = GlobalSettings()


settings = Settings()
logging.config.dictConfig(settings.global_settings.logger_config)
