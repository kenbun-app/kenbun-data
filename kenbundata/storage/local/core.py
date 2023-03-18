import os
from collections.abc import Iterable

from ...encoders import KenbunEncoder
from ...fields import Id
from ...types import Blob, Url
from ..base import BaseStorage
from ..exceptions import UrlNotFoundError
from ..settings import BaseStorageSettings
from .settings import LocalStorageSettings

_encoder = KenbunEncoder()


class LocalStorage(BaseStorage):
    def __init__(self, path: str) -> None:
        super(LocalStorage, self).__init__()
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    def get_url_by_id(self, id: Id) -> Url:
        if not os.path.exists(os.path.join(self.path, "urls", f"{id}.json")):
            raise UrlNotFoundError(id)
        with open(os.path.join(self.path, "urls", f"{id}.json"), "rb") as f:
            return Url.parse_raw(f.read())

    def store_url(self, url: Url) -> None:
        if not os.path.exists(os.path.join(self.path, "urls")):
            os.makedirs(os.path.join(self.path, "urls"))
        with open(os.path.join(self.path, "urls", f"{url.id}.json"), "w", encoding="utf-8") as f:
            f.write(_encoder.encode(url))

    def list_urls(self) -> Iterable[Url]:
        if os.path.exists(os.path.join(self.path, "urls")):
            for filename in os.listdir(os.path.join(self.path, "urls")):
                with open(os.path.join(self.path, "urls", filename), "rb") as f:
                    yield Url.parse_raw(f.read())

    def get_blob_by_id(self, id: Id) -> Blob:
        raise NotImplementedError()

    def store_blob(self, blob: Blob) -> None:
        raise NotImplementedError()

    @classmethod
    def from_settings(cls, settings: BaseStorageSettings) -> "LocalStorage":
        if not isinstance(settings, LocalStorageSettings):
            raise TypeError(f"Expected settings to be LocalStorageSettings, got {type(settings)}")
        return cls(path=settings.path)
