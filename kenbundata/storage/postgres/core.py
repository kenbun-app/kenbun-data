from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ...fields import Id
from ...types import Url
from ..base import BaseStorage
from ..settings import BaseStorageSettings
from . import models
from .settings import PostgresStorageSettings


class PostgresStorage(BaseStorage):
    def __init__(self, postgres_dsn: str) -> None:
        super(PostgresStorage, self).__init__()
        self._postgres_dsn = postgres_dsn
        self._engine = create_engine(self._postgres_dsn)
        self._session_maker = sessionmaker(bind=self._engine)

    @property
    def session(self) -> Generator[Session, None, None]:
        yield self._session_maker()

    @classmethod
    def from_settings(cls, settings: BaseStorageSettings) -> "PostgresStorage":
        if not isinstance(settings, PostgresStorageSettings):
            raise TypeError(f"Expected settings to be PostgresStorageSettings, got {type(settings)}")
        if not settings.sqlalchemy_database_url:
            raise ValueError("SQLAlchemy database URL is not set")
        return cls(postgres_dsn=settings.sqlalchemy_database_url)

    def get_url_by_id(self, id: Id) -> Url:
        with self.session as sess:
            return Url.from_orm(sess.query(models.Url).filter(models.Url.id == id).first())
