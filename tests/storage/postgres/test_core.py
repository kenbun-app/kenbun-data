from typing import List

from kenbundata.fields import Id
from kenbundata.storage.postgres.core import PostgresStorage
from kenbundata.types import Url


def test_get_url_by_id(postgres_storage_fixture: PostgresStorage, url_ids: List[Id], urls_fixture: List[Url]) -> None:
    expected = urls_fixture[0]
    actual = postgres_storage_fixture.get_url_by_id(url_ids[0])
    assert actual == expected
