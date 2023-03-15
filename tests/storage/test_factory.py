from pytest_mock import MockerFixture

from kenbundata.settings import GlobalSettings, StorageType
from kenbundata.storage.factory import create_storage


def test_create_storage_local(mocker: MockerFixture) -> None:
    settings = GlobalSettings(storage_type=StorageType.LOCAL, storage_settings={"path": "/tmp"})
    create_from_global_settings = mocker.patch(
        "kenbundata.storage.factory.LocalStorageSettings.create_from_global_settings"
    )
    from_settings = mocker.patch("kenbundata.storage.factory.LocalStorage.from_settings")
    storage = create_storage(settings=settings)
    from_settings.assert_called_once_with(settings=create_from_global_settings.return_value)
    create_from_global_settings.assert_called_once_with(settings=settings)
    assert storage == from_settings.return_value
