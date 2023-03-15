from collections.abc import MutableMapping
from typing import cast

import pytest
from pydantic import AnyHttpUrl

from kenbundata.fields import Id
from kenbundata.storage.base import BaseStorage
from kenbundata.storage.exceptions import UrlNotFoundError
from kenbundata.storage.settings import BaseStorageSettings
from kenbundata.types import Url


class ConcreteStorage(BaseStorage):
    def __init__(self) -> None:
        self._urls: MutableMapping[Id, Url] = {
            Id("T3HW7dZ5SjCtODQLQkY8eA"): Url(
                id=Id("T3HW7dZ5SjCtODQLQkY8eA"), url=cast(AnyHttpUrl, "https://kenbun.app")
            )
        }

    def get_url_by_id(self, id: Id) -> Url:
        if id not in self._urls:
            raise UrlNotFoundError(id)
        return self._urls[id]

    def store_url(self, url: Url) -> None:
        self._urls[url.id] = url

    @classmethod
    def from_settings(cls, settings: BaseStorageSettings) -> "ConcreteStorage":
        return cls()


def test_get_url_by_id() -> None:
    id_ = Id("T3HW7dZ5SjCtODQLQkY8eA")
    expected = Url(id=id_, url=cast(AnyHttpUrl, "https://kenbun.app"))
    sut = ConcreteStorage()
    actual = sut.get_url_by_id(id_)
    assert actual == expected


def test_get_url_by_id_raises_url_not_found_error() -> None:
    id_ = Id("Xia5PlGDRDCGwaalhXqdww")
    sut = ConcreteStorage()
    with pytest.raises(UrlNotFoundError):
        sut.get_url_by_id(id_)


def test_store_url() -> None:
    id_ = Id("Xia5PlGDRDCGwaalhXqdww")
    url = Url(id=id_, url=cast(AnyHttpUrl, "https://kenbun.app"))
    sut = ConcreteStorage()
    sut.store_url(url)
    actual = sut.get_url_by_id(id_)
    assert actual == url
