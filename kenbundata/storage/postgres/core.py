from collections.abc import Iterable
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from kenbundata.fields import Cursor
from kenbundata.storage.base import IterableWithCursor
from kenbundata.types import Url

from ...fields import Id
from ...types import Blob, Screenshot, Url
from ..base import BaseCursorAwareStorage
from ..exceptions import UrlNotFoundError
from ..settings import BaseStorageSettings
from . import models
from .settings import PostgresStorageSettings


class PostgresStorage(BaseCursorAwareStorage):
    def __init__(self, postgres_dsn: str) -> None:
        super(PostgresStorage, self).__init__()
        self._postgres_dsn = postgres_dsn
        self._engine = create_engine(self._postgres_dsn)

    def __del__(self) -> None:
        self._engine.dispose()

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def session(self) -> Session:
        return Session(self.engine)

    @classmethod
    def from_settings(cls, settings: BaseStorageSettings) -> "PostgresStorage":
        if not isinstance(settings, PostgresStorageSettings):
            raise TypeError(f"Expected settings to be PostgresStorageSettings, got {type(settings)}")
        if not settings.sqlalchemy_database_url:
            raise ValueError("SQLAlchemy database URL is not set")
        return cls(postgres_dsn=settings.sqlalchemy_database_url)

    def get_url_by_id(self, id: Id) -> Url:
        with self.session as sess:
            obj = sess.query(models.Url).filter(models.Url.id == id.uuid).first()
            if not isinstance(obj, models.Url):
                raise UrlNotFoundError(id)
            return Url.from_orm(obj)

    def store_url(self, url: Url) -> None:
        with self.session as sess:
            obj = models.Url(id=url.id.uuid, url=url.url)
            sess.merge(obj)
            sess.commit()

    def list_urls(self) -> Iterable[Url]:
        with self.session as sess:
            for obj in sess.query(models.Url).all():
                yield Url.from_orm(obj)

    def get_blob_by_id(self, id: Id) -> Blob:
        raise NotImplementedError()

    def get_screenshot_by_id(self, id: Id) -> Screenshot:
        raise NotImplementedError()

    def store_blob(self, blob: Blob) -> None:
        raise NotImplementedError()

    def store_screenshot(self, screenshot: Screenshot) -> None:
        raise NotImplementedError()

    def list_urls_with_cursor(self, limit: int, cursor: Optional[Cursor]) -> IterableWithCursor[Url]:
        ...
