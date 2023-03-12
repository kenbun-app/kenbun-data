from pytest_mock import MockerFixture

from kenbundata.settings import GlobalSettings, StorageType
from kenbundata.storage.factory import create_storage


def test_create_storage_local(mocker: MockerFixture) -> None:
    settings = GlobalSettings(storage_type=StorageType.LOCAL, storage_settings={"path": "/tmp"})
    LocalStorage = mocker.patch("kenbundata.storage.factory.LocalStorage")
    storage = create_storage(settings=settings)
    LocalStorage.assert_called_once_with(path="/tmp")
    assert storage == LocalStorage.return_value
