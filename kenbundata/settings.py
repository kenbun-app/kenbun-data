
from enum import Enum
from typing import TypeVar, Union,Annotated

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

from .fields import TypeValueString

S = TypeVar("S", bound="BaseSettings")

class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(env_prefix="KENBUN_", env_file_encoding="utf-8", env_nested_delimiter="__")


class StorageType(TypeValueString, Enum):
    """
    >>> StorageType.LOCAL_FILE == "local_file"
    True
    >>> StorageType.LOCAL_FILE == "postgres"
    False
    >>> StorageType.LOCAL_FILE == "localFile"
    True
    """

    LOCAL_FILE = "local_file"
    POSTGRES = "postgres"


class BaseStorageSettings(BaseSettings):
    storage_type: StorageType


class LocalStorageSettings(BaseStorageSettings):
    storage_type: StorageType = StorageType.LOCAL_FILE
    path: str

class PostgresStorageSettings(BaseStorageSettings):
    storage_type: StorageType = StorageType.POSTGRES
    host: str = 'db'
    username: str = 'postgres'
    password: str
    port: int = 5432
    database: str = 'postgres'

    @computed_field  # type: ignore[misc]
    @property
    def sqlalchemy_database_url(self) -> PostgresDsn:
        return PostgresDsn(
            url=f"postgresql://{self.username}:"
            f"{self.password.replace('@', '%40')}@{self.host}:{self.port}/{self.database}"
        )


StorageSettings = Annotated[Union[LocalStorageSettings, PostgresStorageSettings], Field(discriminator="storage_type")]]


class GlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
