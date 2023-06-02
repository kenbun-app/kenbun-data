from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import Type, TypeVar

from ..fields import Id, Cursor
from ..types import Blob, Screenshot, Url
from .settings import BaseStorageSettings

T = TypeVar("T", bound="BaseStorage")


class BaseStorage(metaclass=ABCMeta):
    @abstractmethod
    def get_url_by_id(self, id: Id) -> Url:
        raise NotImplementedError

    @abstractmethod
    def store_url(self, url: Url) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_urls(self) -> Iterable[Url]:
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


class BaseCursorAwareStorage(BaseStorage):
    @abstractmethod
    def list_urls_with_cursor(self, cursor: Cursor) -> Iterable[Url]:
        raise NotImplementedError
