from pydantic_core import MultiHostUrl

from kenbundata.settings import GlobalSettings, PostgresStorageSettings, StorageType


def test_postgres_storage_settings() -> None:
    sut = PostgresStorageSettings(
        host="localhost",
        port=5432,
        database="kenbun",
        username="kenbunadmin",
        password="superStr0ngPassw0rd",
    )
    assert sut.host == "localhost"
    assert sut.port == 5432
    assert sut.database == "kenbun"
    assert sut.username == "kenbunadmin"
    assert sut.password == "superStr0ngPassw0rd"
    assert sut.sqlalchemy_database_url == MultiHostUrl(
        "postgresql://kenbunadmin:superStr0ngPassw0rd@localhost:5432/kenbun"
    )


def test_postgres_storage_settings_from_global_settings() -> None:
    sut = GlobalSettings(
        storage_settings={
            "storage_type": StorageType.POSTGRES,
            "host": "thedatabase",
            "username": "adminuser",
            "password": "str0ngPassw0rd",
            "port": 54320,
            "database": "kenbundb",
        },
    ).storage_settings
    assert sut.host == "thedatabase"
    assert sut.port == 54320
    assert sut.database == "kenbundb"
    assert sut.username == "adminuser"
    assert sut.password == "str0ngPassw0rd"
    assert sut.sqlalchemy_database_url == MultiHostUrl(
        "postgresql://adminuser:str0ngPassw0rd@thedatabase:54320/kenbundb"
    )


def test_postgres_storage_settings_from_global_settings_default() -> None:
    sut = GlobalSettings(
        storage_settings={
            "storage_type": StorageType.POSTGRES,
            "password": "somepassword",
        },
    ).storage_settings
    assert sut.host == "db"
    assert sut.port == 5432
    assert sut.database == "postgres"
    assert sut.username == "postgres"
    assert sut.password == "somepassword"
    assert sut.sqlalchemy_database_url == MultiHostUrl("postgresql://postgres:somepassword@db:5432/postgres")
