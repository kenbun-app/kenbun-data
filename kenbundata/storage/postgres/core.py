from ..base import BaseStorage
from ..settings import BaseStorageSettings
from .settings import PostgresStorageSettings


class PostgresStorage(BaseStorage):
    def __init__(self, postgres_dsn: str) -> None:
        super(PostgresStorage, self).__init__()
        self._postgres_dsn = postgres_dsn

    @classmethod
    def from_settings(cls, settings: BaseStorageSettings) -> "PostgresStorage":
        if not isinstance(settings, PostgresStorageSettings):
            raise TypeError(f"Expected settings to be PostgresStorageSettings, got {type(settings)}")
        if not settings.sqlalchemy_database_url:
            raise ValueError("SQLAlchemy database URL is not set")
        return cls(postgres_dsn=settings.sqlalchemy_database_url)
