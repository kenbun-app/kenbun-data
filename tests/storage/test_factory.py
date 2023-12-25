from pytest_mock import MockerFixture

from kenbundata.settings import GlobalSettings, StorageType
from kenbundata.storage.factory import create_storage


def test_create_storage_local(mocker: MockerFixture) -> None:
    settings = GlobalSettings(storage_settings={"storage_type": StorageType.LOCAL_FILE, "path": "/tmp"})
    from_settings = mocker.patch("kenbundata.storage.factory.LocalStorage.from_settings")
    storage = create_storage(settings=settings)
    from_settings.assert_called_once_with(settings=settings.storage_settings)
    assert storage == from_settings.return_value


def test_create_storage_postgres(mocker: MockerFixture) -> None:
    settings = GlobalSettings(storage_settings={"storage_type": StorageType.POSTGRES, "password": "passwd"})
    from_settings = mocker.patch("kenbundata.storage.factory.PostgresStorage.from_settings")
    storage = create_storage(settings=settings)
    from_settings.assert_called_once_with(settings=settings.storage_settings)
    assert storage == from_settings.return_value
