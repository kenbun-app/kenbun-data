from kenbundata.settings import GlobalSettings, StorageType
from kenbundata.storage.local.settings import LocalStorageSettings


def test_local_storage_settings() -> None:
    sut = LocalStorageSettings(path="/tmp")
    assert sut.path == "/tmp"


def test_local_storage_settings_from_global_settings() -> None:
    sut = LocalStorageSettings.create_from_global_settings(
        GlobalSettings(storage_type=StorageType.LOCAL, storage_settings={"path": "/tmp"})
    )
    assert sut.path == "/tmp"
