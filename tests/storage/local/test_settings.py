from kenbundata.settings import GlobalSettings, LocalStorageSettings, StorageType


def test_local_storage_settings() -> None:
    sut = LocalStorageSettings(path="/tmp")
    assert sut.path == "/tmp"


def test_local_storage_settings_from_global_settings() -> None:
    sut = GlobalSettings(storage_settings={"storage_type": StorageType.LOCAL_FILE, "path": "/tmp"}).storage_settings

    assert sut.path == "/tmp"
