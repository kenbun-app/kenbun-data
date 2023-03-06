from collections.abc import Mapping
from typing import Optional, cast

from pydantic import PostgresDsn, validator

from ..settings import BaseStorageSettings


class PostgresStorageSettings(BaseStorageSettings):
    host_name: str = 'db'
    user: str = 'postgres'
    password: str
    port: str = '5432'
    database_name: str = 'postgres'
    sqlalchemy_database_url: Optional[PostgresDsn] = None

    @validator("sqlalchemy_database_url", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Mapping[str, str]) -> str:
        if isinstance(v, str):
            return v
        return cast(
            str,
            PostgresDsn.build(
                scheme="postgresql",
                user=values.get("user"),
                password=values.get("password"),
                host=values.get("host_name"),
                port=values.get('port'),
                path=f"/{values.get('database_name') or ''}",
            ),
        )
