from pydantic import PostgresDsn, computed_field

from ...settings import GlobalSettings
from ..settings import BaseStorageSettings


class PostgresStorageSettings(BaseStorageSettings):
    host: str = 'db'
    username: str = 'postgres'
    password: str
    port: int = 5432
    database: str = 'postgres'

    @computed_field  # type: ignore[misc]
    @property
    def sqlalchemy_database_url(self) -> PostgresDsn:
        return PostgresDsn(
            url=f"postgresql://{self.username}:"
            f"{self.password.replace('@', '%40')}@{self.host}:{self.port}/{self.database}"
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
