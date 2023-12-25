from ..settings import GlobalSettings, StorageType
from .base import BaseStorage
from .local import LocalStorage
from .postgres.core import PostgresStorage


def create_storage(settings: GlobalSettings) -> BaseStorage:
    storage_settings = settings.storage_settings
    if storage_settings.storage_type == StorageType.LOCAL_FILE:
        return LocalStorage.from_settings(settings=storage_settings)
    if storage_settings.storage_type == StorageType.POSTGRES:
        return PostgresStorage.from_settings(settings=storage_settings)
    else:
        raise ValueError(f"Unknown storage type: {storage_settings.storage_type}")
