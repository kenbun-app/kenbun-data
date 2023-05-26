from typing import List, cast

import pytest
from pydantic import AnyHttpUrl
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from kenbundata.fields import Id
from kenbundata.storage.exceptions import UrlNotFoundError
from kenbundata.storage.postgres import models
from kenbundata.storage.postgres.core import PostgresStorage
from kenbundata.types import Url


def test_get_url_by_id(postgres_storage_fixture: PostgresStorage, url_ids: List[Id], urls_fixture: List[Url]) -> None:
    expected = urls_fixture[0]
    actual = postgres_storage_fixture.get_url_by_id(url_ids[0])
    assert actual == expected


def test_get_url_by_id_raises_url_not_found_error(postgres_storage_fixture: PostgresStorage) -> None:
    with pytest.raises(UrlNotFoundError):
        postgres_storage_fixture.get_url_by_id(Id("00000000-0000-0000-0000-000000000000"))


def test_store_url(postgres_storage_fixture: PostgresStorage, engine_for_test: Engine) -> None:
    url = Url(id=Id("00000000-0000-0000-0000-000000000000"), url=cast(AnyHttpUrl, "https://example.com"))
    postgres_storage_fixture.store_url(url)
    with Session(engine_for_test) as sess:
        actual = sess.query(models.Url).get(url.id.uuid)
        assert actual is not None
        assert actual.url == url.url


def test_store_url_update(
    postgres_storage_fixture: PostgresStorage, engine_for_test: Engine, url_ids: List[Id]
) -> None:
    url = Url(id=url_ids[0], url=cast(AnyHttpUrl, "https://otherexample.com"))
    postgres_storage_fixture.store_url(url)
    with Session(engine_for_test) as sess:
        actual = sess.query(models.Url).get(url.id.uuid)
        assert actual is not None
        assert actual.url == url.url


def test_list_urls(postgres_storage_fixture: PostgresStorage, urls_fixture: List[Url]) -> None:
    actual = list(postgres_storage_fixture.list_urls())
    assert actual == urls_fixture
