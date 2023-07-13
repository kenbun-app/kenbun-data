import os
from tempfile import TemporaryDirectory
from typing import List

import pytest
from pydantic import AnyHttpUrl

from kenbundata.fields import Bytes, Id, MimeType
from kenbundata.storage.exceptions import (
    BlobNotFoundError,
    ScreenshotNotFoundError,
    UrlNotFoundError,
)
from kenbundata.storage.local import LocalStorage
from kenbundata.types import Blob, Screenshot, TargetUrl

wd = os.path.dirname(os.path.abspath(__file__))
fixture_path = os.path.join(wd, "fixtures")


def test_local_storage_settings() -> None:
    sut = LocalStorage(path="/tmp")
    assert sut.path == "/tmp"


def test_local_storage_get_url_by_id() -> None:
    sut = LocalStorage(path=fixture_path)
    expected = TargetUrl(id=Id("xAxynPxZSKa_t6ljybzkHg"), url=AnyHttpUrl("https://kenbun.app"))
    actual = sut.get_url_by_id(id=Id("xAxynPxZSKa_t6ljybzkHg"))
    assert actual == expected


def test_local_storage_get_url_by_id_raises_url_not_found_error() -> None:
    sut = LocalStorage(path=fixture_path)
    with pytest.raises(UrlNotFoundError):
        sut.get_url_by_id(id=Id("koy3tQwzSc6I26fkG-H7LQ"))


def test_local_storage_store_url() -> None:
    with TemporaryDirectory() as tmpdir:
        sut = LocalStorage(path=tmpdir)
        url = TargetUrl(id=Id("xAxynPxZSKa_t6ljybzkHg"), url=AnyHttpUrl("https://kenbun.app"))
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
        TargetUrl(id=Id("xAxynPxZSKa_t6ljybzkHg"), url=AnyHttpUrl("https://kenbun.app")),
        TargetUrl(id=Id("uVbjm2k3RGu0nilH1ydlMQ"), url=AnyHttpUrl("https://osoken.ai")),
    ]
    actual = list(sut.list_urls())
    assert all(a in expected for a in actual) and all(e in actual for e in expected) and len(actual) == len(expected)


def test_local_storage_list_urls_empty() -> None:
    with TemporaryDirectory() as tmpdir:
        sut = LocalStorage(path=tmpdir)
        expected: List[TargetUrl] = []
        actual = list(sut.list_urls())
        assert actual == expected


def test_local_storage_get_blob_by_id() -> None:
    sut = LocalStorage(path=fixture_path)
    id_ = Id("JSxa9P6_Qjij1P1WPE7g4g")
    expected = Blob(id=id_, data=Bytes("YWFh"), mime_type=MimeType("text/plain"))
    actual = sut.get_blob_by_id(id_)
    assert actual == expected


def test_local_storage_get_blob_by_id_raises_blob_not_found_error() -> None:
    sut = LocalStorage(path=fixture_path)
    with pytest.raises(BlobNotFoundError):
        sut.get_blob_by_id(Id("koy3tQwzSc6I26fkG-H7LQ"))


def test_local_storage_store_blob() -> None:
    with TemporaryDirectory() as tmpdir:
        sut = LocalStorage(path=tmpdir)
        blob = Blob(id=Id("JSxa9P6_Qjij1P1WPE7g4g"), data=Bytes("YWFh"), mime_type=MimeType("text/plain"))
        sut.store_blob(blob=blob)
        with open(os.path.join(fixture_path, "blobs", "JSxa9P6_Qjij1P1WPE7g4g.json"), "r") as f:
            expected = f.read()
        assert os.path.exists(os.path.join(tmpdir, "blobs", "JSxa9P6_Qjij1P1WPE7g4g.json"))
        with open(os.path.join(tmpdir, "blobs", "JSxa9P6_Qjij1P1WPE7g4g.json"), "r") as f:
            actual = f.read()
        assert actual == expected


def test_local_storage_get_screenshot_by_id() -> None:
    sut = LocalStorage(path=fixture_path)
    id_ = Id("80pExMLSTDS-VCLOIK4_Pg")
    with open(os.path.join(fixture_path, "screenshots", "80pExMLSTDS-VCLOIK4_Pg.json"), "r") as f:
        expected = Screenshot.model_validate_json(f.read())
    actual = sut.get_screenshot_by_id(id_)
    assert actual == expected


def test_local_storage_get_screenshot_by_id_raises_screenshot_not_found_error() -> None:
    sut = LocalStorage(path=fixture_path)
    with pytest.raises(ScreenshotNotFoundError):
        sut.get_screenshot_by_id(Id("koy3tQwzSc6I26fkG-H7LQ"))


def test_local_storage_store_screenshot() -> None:
    with TemporaryDirectory() as tmpdir:
        sut = LocalStorage(path=tmpdir)
        with open(os.path.join(fixture_path, "screenshots", "80pExMLSTDS-VCLOIK4_Pg.json"), "r") as f:
            screenshot = Screenshot.model_validate_json(f.read())
        sut.store_screenshot(screenshot=screenshot)
        with open(os.path.join(fixture_path, "screenshots", "80pExMLSTDS-VCLOIK4_Pg.json"), "r") as f:
            expected = f.read()
        assert os.path.exists(os.path.join(tmpdir, "screenshots", "80pExMLSTDS-VCLOIK4_Pg.json"))
        with open(os.path.join(tmpdir, "screenshots", "80pExMLSTDS-VCLOIK4_Pg.json"), "r") as f:
            actual = f.read()
        assert actual == expected
