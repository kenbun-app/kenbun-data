from json import JSONEncoder
from typing import Any

from .fields import Bytes, Id
from .schema import BaseModel


class KenbunEncoder(JSONEncoder):
    """
    >>> from kenbundata.fields import MimeType, Timestamp
    >>> a = {"id": Id("T3HW7dZ5SjCtODQLQkY8eA"), "data": Bytes(b"kenbun"), "type": MimeType("text/plain"), "created_at": Timestamp(1610000000)}
    >>> KenbunEncoder().encode(a)
    '{"id": "T3HW7dZ5SjCtODQLQkY8eA", "data": "a2VuYnVu", "type": "text/plain", "created_at": 1610000000}'
    """  # noqa: E501

    def default(self, o: Any) -> Any:
        if isinstance(o, BaseModel):
            return o.dict()
        if isinstance(o, Bytes):
            return o.b64urlencoded
        if isinstance(o, Id):
            return o.b64encoded
        return super().default(o)
