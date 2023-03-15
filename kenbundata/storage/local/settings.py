from ...settings import GlobalSettings
from ..settings import BaseStorageSettings


class LocalStorageSettings(BaseStorageSettings):
    path: str

    @classmethod
    def from_global_settings(cls, settings: GlobalSettings) -> "LocalStorageSettings":
        path = settings.storage_settings["path"]
        if not isinstance(path, str):
            raise ValueError(f"Invalid path: {path}")
        return cls(path=path)
