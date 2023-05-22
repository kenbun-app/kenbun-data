from typing import List

import pytest

from kenbundata.fields import Id
from kenbundata.storage.exceptions import UrlNotFoundError
from kenbundata.storage.postgres.core import PostgresStorage
from kenbundata.types import Url


def test_get_url_by_id(postgres_storage_fixture: PostgresStorage, url_ids: List[Id], urls_fixture: List[Url]) -> None:
    expected = urls_fixture[0]
    actual = postgres_storage_fixture.get_url_by_id(url_ids[0])
    assert actual == expected


def test_get_url_by_id_raises_url_not_found_error(postgres_storage_fixture: PostgresStorage) -> None:
    with pytest.raises(UrlNotFoundError):
        postgres_storage_fixture.get_url_by_id(Id("00000000-0000-0000-0000-000000000000"))
