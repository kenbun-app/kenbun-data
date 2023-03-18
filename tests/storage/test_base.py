from collections.abc import Iterable, MutableMapping
from typing import cast

import pytest
from pydantic import AnyHttpUrl

from kenbundata.fields import Bytes, Id, MimeType
from kenbundata.storage.base import BaseStorage
from kenbundata.storage.exceptions import BlobNotFoundError, UrlNotFoundError
from kenbundata.storage.settings import BaseStorageSettings
from kenbundata.types import Blob, Url


class ConcreteStorage(BaseStorage):
    def __init__(self) -> None:
        self._urls: MutableMapping[Id, Url] = {
            Id("T3HW7dZ5SjCtODQLQkY8eA"): Url(
                id=Id("T3HW7dZ5SjCtODQLQkY8eA"), url=cast(AnyHttpUrl, "https://kenbun.app")
            )
        }
        self._blobs: MutableMapping[Id, Blob] = {
            Id("8bbz-1tVSGqlVU7_zvomqg"): Blob(
                id=Id('8bbz-1tVSGqlVU7_zvomqg'), data=Bytes(b'aaa'), mime_type=MimeType.text_plain
            )
        }

    def get_url_by_id(self, id: Id) -> Url:
        if id not in self._urls:
            raise UrlNotFoundError(id)
        return self._urls[id]

    def store_url(self, url: Url) -> None:
        self._urls[url.id] = url

    def list_urls(self) -> Iterable[Url]:
        return iter(list(self._urls.values()))

    def get_blob_by_id(self, id: Id) -> Blob:
        if id not in self._blobs:
            raise BlobNotFoundError(id)
        return self._blobs[id]

    def store_blob(self, blob: Blob) -> None:
        self._blobs[blob.id] = blob

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


def test_list_urls() -> None:
    id_ = Id("T3HW7dZ5SjCtODQLQkY8eA")
    expected = [Url(id=id_, url=cast(AnyHttpUrl, "https://kenbun.app"))]
    sut = ConcreteStorage()
    actual = list(sut.list_urls())
    assert actual == expected


def test_get_blob_by_id() -> None:
    id_ = Id("8bbz-1tVSGqlVU7_zvomqg")
    expected = Blob(id=id_, data=Bytes(b'aaa'), mime_type=MimeType.text_plain)
    sut = ConcreteStorage()
    actual = sut.get_blob_by_id(id_)
    assert actual == expected


def test_store_blob() -> None:
    id_ = Id("ltv5IY6LTpmIIf1QWeGNGw")
    blob = Blob(id=Id('ltv5IY6LTpmIIf1QWeGNGw'), data=Bytes(b'bbb'), mime_type=MimeType.text_plain)
    sut = ConcreteStorage()
    sut.store_blob(blob)
    actual = sut.get_blob_by_id(id_)
    assert actual == blob


def test_get_blob_by_id_raises_blob_not_found_error() -> None:
    id_ = Id("ltv5IY6LTpmIIf1QWeGNGw")
    sut = ConcreteStorage()
    with pytest.raises(BlobNotFoundError):
        sut.get_blob_by_id(id_)
