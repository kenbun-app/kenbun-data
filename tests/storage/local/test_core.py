import os
from tempfile import TemporaryDirectory
from typing import List, cast

import pytest
from pydantic import AnyHttpUrl

from kenbundata.fields import Bytes, Id, MimeType
from kenbundata.storage.exceptions import UrlNotFoundError
from kenbundata.storage.local import LocalStorage
from kenbundata.types import Blob, Url

wd = os.path.dirname(os.path.abspath(__file__))
fixture_path = os.path.join(wd, "fixtures")


def test_local_storage_settings() -> None:
    sut = LocalStorage(path="/tmp")
    assert sut.path == "/tmp"


def test_local_storage_get_url_by_id() -> None:
    sut = LocalStorage(path=fixture_path)
    expected = Url(id=Id("xAxynPxZSKa_t6ljybzkHg"), url=cast(AnyHttpUrl, "https://kenbun.app"))
    actual = sut.get_url_by_id(id=Id("xAxynPxZSKa_t6ljybzkHg"))
    assert actual == expected


def test_local_storage_get_url_by_id_raises_url_not_found_error() -> None:
    sut = LocalStorage(path=fixture_path)
    with pytest.raises(UrlNotFoundError):
        sut.get_url_by_id(id=Id("koy3tQwzSc6I26fkG-H7LQ"))


def test_local_storage_store_url() -> None:
    with TemporaryDirectory() as tmpdir:
        sut = LocalStorage(path=tmpdir)
        url = Url(id=Id("xAxynPxZSKa_t6ljybzkHg"), url=cast(AnyHttpUrl, "https://kenbun.app"))
        sut.store_url(url=url)
        with open(os.path.join(fixture_path, "urls", "xAxynPxZSKa_t6ljybzkHg.json"), "r") as f:
            expected = f.read()
        assert os.path.exists(os.path.join(tmpdir, "urls", "xAxynPxZSKa_t6ljybzkHg.json"))
        with open(os.path.join(tmpdir, "urls", "xAxynPxZSKa_t6ljybzkHg.json"), "r") as f:
            actual = f.read()
        assert actual == expected


def test_local_storage_list_urls() -> None:
    sut = LocalStorage(path=fixture_path)
    expected = [
        Url(id=Id("xAxynPxZSKa_t6ljybzkHg"), url=cast(AnyHttpUrl, "https://kenbun.app")),
        Url(id=Id("uVbjm2k3RGu0nilH1ydlMQ"), url=cast(AnyHttpUrl, "https://osoken.ai")),
    ]
    actual = list(sut.list_urls())
    assert all(a in expected for a in actual) and all(e in actual for e in expected) and len(actual) == len(expected)


def test_local_storage_list_urls_empty() -> None:
    with TemporaryDirectory() as tmpdir:
        sut = LocalStorage(path=tmpdir)
        expected: List[Url] = []
        actual = list(sut.list_urls())
        assert actual == expected


def test_local_storage_get_blob_by_id() -> None:
    sut = LocalStorage(path=fixture_path)
    id_ = Id("JSxa9P6_Qjij1P1WPE7g4g")
    expected = Blob(id=id_, data=Bytes("YWFh"), mime_type=MimeType.text_plain)
    actual = sut.get_blob_by_id(id_)
    assert actual == expected
