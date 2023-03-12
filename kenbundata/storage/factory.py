from ..settings import GlobalSettings, StorageType
from .base import BaseStorage
from .local import LocalStorage, LocalStorageSettings


def create_storage(settings: GlobalSettings) -> BaseStorage:
    if settings.storage_type == StorageType.LOCAL:
        local_settings = LocalStorageSettings.create_from_global_settings(settings=settings)
        return LocalStorage(path=local_settings.path)
    else:
        raise ValueError(f"Unknown storage type: {settings.storage_type}")
