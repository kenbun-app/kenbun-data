from collections.abc import Generator
from typing import List, cast

import pytest
from pydantic import AnyHttpUrl
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from kenbundata.fields import Id
from kenbundata.storage.postgres import models
from kenbundata.storage.postgres.core import PostgresStorage
from kenbundata.storage.postgres.settings import PostgresStorageSettings
from kenbundata.types import Url

TEST_DATABASE_NAME = "test"


def create_engine_from_settings(settings: PostgresStorageSettings) -> Engine:
    if not settings.sqlalchemy_database_url:
        raise ValueError("SQLAlchemy database URL is not set")
    return create_engine(settings.sqlalchemy_database_url)


@pytest.fixture(scope="session")
def settings_for_default() -> Generator[PostgresStorageSettings, None, None]:
    settings = PostgresStorageSettings(
        host="127.0.0.1", port=5432, username="postgres", password="postgres", database="postgres"
    )
    yield settings


@pytest.fixture(scope="session")
def settings_for_test() -> Generator[PostgresStorageSettings, None, None]:
    settings = PostgresStorageSettings(
        host="127.0.0.1", port=5432, username="postgres", password="postgres", database=TEST_DATABASE_NAME
    )
    yield settings


@pytest.fixture(scope="session")
def db_for_test(settings_for_default: PostgresStorageSettings) -> Generator[int, None, None]:
    engine = create_engine_from_settings(settings_for_default)
    conn = engine.connect()
    conn.execute(text("commit"))
    try:
        conn.execute(text("drop database test"))
    except SQLAlchemyError:
        pass
    finally:
        conn.close()

    conn = engine.connect()
    conn.execute(text("commit"))
    conn.execute(text("create database test"))
    conn.close()

    yield 1

    conn = engine.connect()
    conn.execute(text("commit"))
    conn.execute(text("drop database test"))
    conn.close()

    engine.dispose()


@pytest.fixture(scope="session")
def engine_for_test(settings_for_test: PostgresStorageSettings, db_for_test: int) -> Generator[Engine, None, None]:
    engine = create_engine_from_settings(settings_for_test)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def schema_for_test(settings_for_test: PostgresStorageSettings, db_for_test: int) -> Generator[int, None, None]:
    engine = create_engine_from_settings(settings_for_test)
    models.Base.metadata.create_all(engine)

    yield 1
    engine.dispose()


@pytest.fixture(scope="session")
def postgres_storage_fixture(
    settings_for_test: PostgresStorageSettings, schema_for_test: int
) -> Generator[PostgresStorage, None, None]:
    yield PostgresStorage.from_settings(settings_for_test)


@pytest.fixture(scope="session")
def url_ids() -> Generator[List[Id], None, None]:
    yield [Id("uVbjm2k3RGu0nilH1ydlMQ"), Id("xAxynPxZSKa_t6ljybzkHg")]


@pytest.fixture(scope="function")
def urls_fixture(
    postgres_storage_fixture: PostgresStorage, settings_for_test: PostgresStorageSettings, url_ids: List[Id]
) -> Generator[List[Url], None, None]:
    engine = create_engine_from_settings(settings_for_test)
    with Session(engine) as session:
        session.query(models.Url).delete()
        session.add_all(
            [
                models.Url(id=url_ids[0].uuid, url="https://osoken.ai"),
                models.Url(id=url_ids[1].uuid, url="https://kenbun.app"),
            ]
        )
        session.commit()
    yield [
        Url(id=url_ids[0], url=cast(AnyHttpUrl, "https://osoken.ai")),
        Url(id=url_ids[1], url=cast(AnyHttpUrl, "https://kenbun.app")),
    ]
    engine.dispose()
