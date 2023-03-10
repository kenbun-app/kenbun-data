from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from enum import Enum
from typing import Any, TypeVar

from pydantic import BaseSettings as _BaseSettings

S = TypeVar("S", bound="BaseSettings")


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


class BaseComponentSettings(BaseSettings, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create_from_global_settings(cls: type[S], settings: GlobalSettings) -> S:
        raise NotImplementedError
