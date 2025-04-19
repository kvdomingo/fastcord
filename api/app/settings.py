from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHON_ENV: Literal["development", "production"] = "production"
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    SECRET_KEY: str

    DEFAULT_SESSION_DURATION_MINUTES: int = 60

    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DATABASE: str
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int = 5432

    STYTCH_PROJECT_ID: str
    STYTCH_SECRET: str
    STYTCH_PUBLIC_TOKEN: str
    STYTCH_ENVIRONMENT: Literal["test", "live"]

    @computed_field
    @property
    def IN_PRODUCTION(self) -> bool:
        return self.PYTHON_ENV == "production"

    @computed_field
    @property
    def DATABASE_CONN_PARAMS(self) -> dict[str, str | int]:
        return {
            "username": self.POSTGRESQL_USERNAME,
            "password": self.POSTGRESQL_PASSWORD,
            "path": self.POSTGRESQL_DATABASE,
            "host": self.POSTGRESQL_HOST,
            "port": self.POSTGRESQL_PORT,
        }

    @computed_field
    @property
    def DATABASE_URL_ASYNC(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                **self.DATABASE_CONN_PARAMS,
            )
        )

    @computed_field
    @property
    def DATABASE_URL_SYNC(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                **self.DATABASE_CONN_PARAMS,
            )
        )


@lru_cache
def _get_settings():
    return Settings()


settings = _get_settings()
