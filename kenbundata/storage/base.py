from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import Generic, Optional, Type, TypeVar

from ..fields import Cursor, Id
from ..types import BaseEntity, BaseModel, Blob, Screenshot, TargetUrl
from .settings import BaseStorageSettings

T = TypeVar("T", bound="BaseStorage")


class BaseStorage(metaclass=ABCMeta):
    @abstractmethod
    def get_url_by_id(self, id: Id) -> TargetUrl:
        raise NotImplementedError

    @abstractmethod
    def store_url(self, url: TargetUrl) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_urls(self) -> Iterable[TargetUrl]:
        raise NotImplementedError

    @abstractmethod
    def get_blob_by_id(self, id: Id) -> Blob:
        raise NotImplementedError

    @abstractmethod
    def store_blob(self, blob: Blob) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_screenshot_by_id(self, id: Id) -> Screenshot:
        raise NotImplementedError

    @abstractmethod
    def store_screenshot(self, screenshot: Screenshot) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_settings(cls: Type[T], settings: BaseStorageSettings) -> T:
        raise NotImplementedError


E = TypeVar("E", bound="BaseEntity")


class ListMetadata(BaseModel):
    next_cursor: Optional[Cursor]
    prev_cursor: Optional[Cursor]


class IterableWithCursor(BaseModel, Generic[E]):
    items: Iterable[E]
    metadata: ListMetadata


class BaseCursorAwareStorage(BaseStorage):
    @abstractmethod
    def list_urls_with_cursor(self, cursor: Optional[Cursor] = None, limit: int = 10) -> IterableWithCursor[TargetUrl]:
        raise NotImplementedError
