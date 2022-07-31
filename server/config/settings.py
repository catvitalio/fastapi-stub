from enum import Enum
from multiprocessing import cpu_count
from typing import Any, Optional

from pydantic import AnyHttpUrl, BaseSettings, Field, PostgresDsn, validator


class LogLevel(str, Enum):
    NOTSET = 'notset'
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    FATAL = 'fatal'


class Settings(BaseSettings):
    DEBUG: bool = Field(..., env='DEBUG')

    HOST: str = '0.0.0.0'
    PORT: int = 8000
    RELOAD: bool = DEBUG
    WORKERS_COUNT: int = 1 if DEBUG else cpu_count() * 2 + 1
    LOG_LEVEL: LogLevel = LogLevel.DEBUG if DEBUG else LogLevel.INFO

    CORS_ALLOWED_ORIGINS: list[AnyHttpUrl] = Field(..., env='CORS_ALLOWED_ORIGINS')

    @validator('CORS_ALLOWED_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_HOST: str = Field(..., env='POSTGRES_HOST')
    POSTGRES_USER: str = Field(..., env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(..., env='POSTGRES_PASSWORD')
    POSTGRES_DB: str = Field(..., env='POSTGRES_DB')
    DATABASE_URI: Optional[PostgresDsn] = None
    DATABASE_ECHO: bool = False

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            path=f'/{values.get("POSTGRES_DB") or ""}',
        )

    class Config:
        case_sensitive = True
