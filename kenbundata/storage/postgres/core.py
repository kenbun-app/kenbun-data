from collections.abc import Iterable
from typing import Optional, Union, cast

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Query, Session

from ...fields import Cursor, CursorValue, Id
from ...types import Blob, Screenshot, TargetUrl
from ..base import BaseCursorAwareStorage, IterableWithCursor, ListMetadata
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
        return cls(postgres_dsn=settings.sqlalchemy_database_url.unicode_string())

    def get_url_by_id(self, id: Id) -> TargetUrl:
        with self.session as sess:
            obj = sess.query(models.Url).filter(models.Url.id == id.uuid).first()
            if not isinstance(obj, models.Url):
                raise UrlNotFoundError(id)
            return TargetUrl.model_validate(obj)

    def store_url(self, url: TargetUrl) -> None:
        with self.session as sess:
            obj = models.Url(id=url.id.uuid, url=url.url.unicode_string())
            sess.merge(obj)
            sess.commit()

    def list_urls(self) -> Iterable[TargetUrl]:
        with self.session as sess:
            for obj in sess.query(models.Url).all():
                yield TargetUrl.model_validate(obj)

    def get_blob_by_id(self, id: Id) -> Blob:
        raise NotImplementedError()

    def get_screenshot_by_id(self, id: Id) -> Screenshot:
        raise NotImplementedError()

    def store_blob(self, blob: Blob) -> None:
        raise NotImplementedError()

    def store_screenshot(self, screenshot: Screenshot) -> None:
        raise NotImplementedError()

    def list_urls_with_cursor(self, cursor: Optional[Cursor] = None, limit: int = 10) -> IterableWithCursor[TargetUrl]:
        with self.session as sess:
            query = sess.query(models.Url)
            invert = False
            if cursor:
                if cursor.is_next():
                    query = query.order_by(models.Url.cursor_value.desc()).filter(
                        models.Url.cursor_value < cursor.value
                    )
                else:
                    query = query.order_by(models.Url.cursor_value.asc()).filter(models.Url.cursor_value > cursor.value)
                    invert = True
            else:
                query = query.order_by(models.Url.cursor_value.desc())
            items = list(query.all()[:limit])
            if len(items) == 0:
                return IterableWithCursor(items=[], metadata=ListMetadata(next_cursor=None, prev_cursor=None))
            if invert:
                items.reverse()
            return IterableWithCursor(
                items=[TargetUrl.model_validate(d) for d in items],
                metadata=ListMetadata(
                    next_cursor=self._url_get_next_cursor_if_exists(sess, query, items[-1]),
                    prev_cursor=self._url_get_prev_cursor_if_exists(sess, query, items[0]),
                ),
            )

    def _url_has_next(self, sess: Session, query: Query[models.Url], url: models.Url) -> bool:
        return cast(bool, sess.query(query.filter(models.Url.cursor_value < url.cursor_value).exists()).scalar())

    def _url_has_prev(self, sess: Session, query: Query[models.Url], url: models.Url) -> bool:
        return cast(bool, sess.query(query.filter(models.Url.cursor_value > url.cursor_value).exists()).scalar())

    def _url_get_next_cursor_if_exists(
        self, sess: Session, query: Query[models.Url], url: models.Url
    ) -> Union[Cursor, None]:
        return (
            Cursor.from_value(CursorValue(cast(str, url.cursor_value)), Cursor.Direction.NEXT)
            if self._url_has_next(sess, query, url)
            else None
        )

    def _url_get_prev_cursor_if_exists(
        self, sess: Session, query: Query[models.Url], url: models.Url
    ) -> Union[Cursor, None]:
        return (
            Cursor.from_value(CursorValue(cast(str, url.cursor_value)), Cursor.Direction.PREV)
            if self._url_has_next(sess, query, url)
            else None
        )
