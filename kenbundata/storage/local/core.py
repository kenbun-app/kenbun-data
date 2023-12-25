import os
from collections.abc import Iterable

from ...fields import Id
from ...settings import BaseStorageSettings, LocalStorageSettings
from ...types import Blob, Screenshot, TargetUrl
from ..base import BaseStorage
from ..exceptions import BlobNotFoundError, ScreenshotNotFoundError, UrlNotFoundError


class LocalStorage(BaseStorage):
    def __init__(self, path: str) -> None:
        super(LocalStorage, self).__init__()
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    def get_url_by_id(self, id: Id) -> TargetUrl:
        if not os.path.exists(os.path.join(self.path, "urls", f"{id}.json")):
            raise UrlNotFoundError(id)
        with open(os.path.join(self.path, "urls", f"{id}.json"), "rb") as f:
            return TargetUrl.model_validate_json(f.read())

    def store_url(self, url: TargetUrl) -> None:
        if not os.path.exists(os.path.join(self.path, "urls")):
            os.makedirs(os.path.join(self.path, "urls"))
        with open(os.path.join(self.path, "urls", f"{url.id}.json"), "w", encoding="utf-8") as f:
            f.write(url.model_dump_json())

    def list_urls(self) -> Iterable[TargetUrl]:
        if os.path.exists(os.path.join(self.path, "urls")):
            for filename in os.listdir(os.path.join(self.path, "urls")):
                with open(os.path.join(self.path, "urls", filename), "rb") as f:
                    yield TargetUrl.model_validate_json(f.read())

    def get_blob_by_id(self, id: Id) -> Blob:
        if not os.path.exists(os.path.join(self.path, "blobs", f"{id}.json")):
            raise BlobNotFoundError(id)
        with open(os.path.join(self.path, "blobs", f"{id}.json"), "rb") as f:
            return Blob.model_validate_json(f.read())

    def store_blob(self, blob: Blob) -> None:
        if not os.path.exists(os.path.join(self.path, "blobs")):
            os.makedirs(os.path.join(self.path, "blobs"))
        with open(os.path.join(self.path, "blobs", f"{blob.id}.json"), "w", encoding="utf-8") as f:
            f.write(blob.model_dump_json())

    @classmethod
    def from_settings(cls, settings: BaseStorageSettings) -> "LocalStorage":
        if not isinstance(settings, LocalStorageSettings):
            raise TypeError(f"Expected settings to be LocalStorageSettings, got {type(settings)}")
        return cls(path=settings.path)

    def get_screenshot_by_id(self, id: Id) -> Screenshot:
        if not os.path.exists(os.path.join(self.path, "screenshots", f"{id}.json")):
            raise ScreenshotNotFoundError(id)
        with open(os.path.join(self.path, "screenshots", f"{id}.json"), "rb") as f:
            return Screenshot.model_validate_json(f.read())

    def store_screenshot(self, screenshot: Screenshot) -> None:
        if not os.path.exists(os.path.join(self.path, "screenshots")):
            os.makedirs(os.path.join(self.path, "screenshots"))
        with open(
            os.path.join(self.path, "screenshots", f"{screenshot.id}.json"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(screenshot.model_dump_json())
