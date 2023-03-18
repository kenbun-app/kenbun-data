from typing import Type

from ..exceptions import BaseError
from ..fields import Id
from ..types import BaseModel, Blob, Url


class StorageError(BaseError):
    """Base exception class for storage errors."""

    pass


class EntityNotFoundError(StorageError, KeyError):
    """Raised when an entity is not found in storage."""

    def __init__(self, entity_id: Id, type: Type[BaseModel]):
        super().__init__(f"{type.__name__} with ID {entity_id} not found")


class UrlNotFoundError(EntityNotFoundError):
    """Raised when a URL is not found in storage."""

    def __init__(self, url_id: Id):
        super().__init__(url_id, Url)


class BlobNotFoundError(EntityNotFoundError):
    """Raised when a blob is not found in storage."""

    def __init__(self, blob_id: Id):
        super().__init__(blob_id, Blob)
