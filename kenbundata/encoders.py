from json import JSONEncoder
from typing import Any

from .fields import Serializable
from .types import BaseModel


class KenbunEncoder(JSONEncoder):
    """
    >>> from kenbundata.fields import MimeType, Timestamp, Bytes, Id
    >>> a = {"id": Id("T3HW7dZ5SjCtODQLQkY8eA"), "data": Bytes(b"kenbun"), "type": MimeType("text/plain"), "created_at": Timestamp(1610000000)}
    >>> KenbunEncoder().encode(a)
    '{"id": "T3HW7dZ5SjCtODQLQkY8eA", "data": "a2VuYnVu", "type": "text/plain", "created_at": 1610000000}'
    >>> class A(BaseModel):
    ...     id: Id
    ...     data: Bytes
    ...     type: MimeType
    ...     created_at: Timestamp
    >>> a = A(**a)
    >>> KenbunEncoder().encode(a)
    '{"id": "T3HW7dZ5SjCtODQLQkY8eA", "data": "a2VuYnVu", "type": "text/plain", "createdAt": 1610000000}'
    """  # noqa: E501

    def default(self, o: Any) -> Any:
        if isinstance(o, BaseModel):
            return o.dict()
        if isinstance(o, Serializable):
            return o.serialize()
        return super().default(o)
