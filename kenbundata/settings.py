from collections.abc import Mapping
from enum import Enum
from typing import Any

from pydantic import BaseSettings as _BaseSettings


class StorageType(str, Enum):
    LOCAL = "local"
    POSTGRES = "postgres"


class BaseSettings(_BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


class GlobalSettings(BaseSettings):
    storage_type: StorageType = StorageType.LOCAL
    storage_settings: Mapping[str, Any] = {}
