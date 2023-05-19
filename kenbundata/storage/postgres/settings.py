from collections.abc import Mapping
from typing import Optional, cast

from pydantic import PostgresDsn, validator

from ...settings import GlobalSettings
from ..settings import BaseStorageSettings


class PostgresStorageSettings(BaseStorageSettings):
    host: str = 'db'
    username: str = 'postgres'
    password: str
    port: int = 5432
    database: str = 'postgres'
    sqlalchemy_database_url: Optional[PostgresDsn] = None

    @validator("sqlalchemy_database_url", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Mapping[str, str]) -> str:
        if isinstance(v, str):
            return v
        return cast(
            str,
            PostgresDsn.build(
                scheme="postgresql",
                user=values.get("username"),
                password=values.get("password"),
                host=values.get("host"),
                port=str(values.get('port')),
                path=f"/{values.get('database') or ''}",
            ),
        )

    @classmethod
    def from_global_settings(cls, settings: GlobalSettings) -> "PostgresStorageSettings":
        return cls(
            host=settings.storage_settings.get("host", "db"),
            port=settings.storage_settings.get("port", 5432),
            database=settings.storage_settings.get("database", "postgres"),
            username=settings.storage_settings.get("username", "postgres"),
            password=str(settings.storage_settings.get("password")),
        )
