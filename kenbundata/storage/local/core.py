import os

from ...encoders import KenbunEncoder
from ...fields import Id
from ...schema import Url
from ..base import BaseStorage
from ..exceptions import UrlNotFoundError

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
