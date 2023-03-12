import os
from tempfile import TemporaryDirectory
from typing import cast

from pydantic import AnyHttpUrl

from kenbundata.fields import Id
from kenbundata.schema import Url
from kenbundata.storage.local import LocalStorage

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
