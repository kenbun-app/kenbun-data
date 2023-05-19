from ..settings import GlobalSettings, StorageType
from .base import BaseStorage
from .local import LocalStorage, LocalStorageSettings
from .postgres.core import PostgresStorage
from .postgres.settings import PostgresStorageSettings


def create_storage(settings: GlobalSettings) -> BaseStorage:
    if settings.storage_type == StorageType.LOCAL:
        local_settings = LocalStorageSettings.from_global_settings(settings=settings)
        return LocalStorage.from_settings(settings=local_settings)
    if settings.storage_type == StorageType.POSTGRES:
        return PostgresStorage.from_settings(settings=PostgresStorageSettings.from_global_settings(settings=settings))
    else:
        raise ValueError(f"Unknown storage type: {settings.storage_type}")
