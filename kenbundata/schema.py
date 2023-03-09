from collections.abc import Mapping
from typing import AbstractSet, Any, Dict, Optional, Union

from pydantic import AnyHttpUrl
from pydantic import BaseModel as _BaseModel
from pydantic import Field

from .fields import Id, MimeType
from .utils import Camelizer


class BaseModel(_BaseModel):
    """Base model for all models in kenbun.
    >>> from unittest.mock import patch
    >>> class MyModel(BaseModel):
    ...     name: str
    ...     url: str
    ...
    >>> with patch.object(MyModel.__fields__["id"], "default_factory", return_value=Id("T3HW7dZ5SjCtODQLQkY8eA")):
    ...     MyModel(name="kenbun", url="https://kenbun.app")
    ...
    MyModel(id=Id('T3HW7dZ5SjCtODQLQkY8eA'), name='kenbun', url='https://kenbun.app')
    >>>
    """

    id: Id = Field(default_factory=Id.generate)

    class Config:
        allow_mutation = False
        alias_generator = Camelizer(["url", "ip", "id"])
        allow_population_by_field_name = True

    def dict(
        self,
        *,
        include: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], None] = None,
        exclude: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any], None] = None,
        by_alias: bool = True,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        """serialize returns a dict representation of the model.
        >>> from unittest.mock import patch
        >>> class MyModel(BaseModel):
        ...     friend_id: Id
        ...     name: str
        ...     base_url: str
        ...     two_words: str
        ...
        >>> with patch.object(MyModel.__fields__["id"], "default_factory", return_value=Id("XsSoTH9cQzyT1xVxxxctNg")):
        ...     MyModel(friend_id=Id("fLb3LTy4RsOADmV1rkR2pA"), name="kenbun", base_url="https://kenbun.app", two_words="aaa").dict()
        ...
        {'id': Id('XsSoTH9cQzyT1xVxxxctNg'), 'friendID': Id('fLb3LTy4RsOADmV1rkR2pA'), 'name': 'kenbun', 'baseURL': 'https://kenbun.app', 'twoWords': 'aaa'}
        """  # noqa: E501
        return super(BaseModel, self).dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )


class Url(BaseModel):
    """Data model represents URL
    >>> from unittest.mock import patch
    >>> with patch.object(Url.__fields__["id"], "default_factory", return_value=Id("zegKeMRzTSux24g3kzp6nw")):
    ...     Url(url="https://kenbun.app")
    ...
    Url(id=Id('zegKeMRzTSux24g3kzp6nw'), url=AnyHttpUrl('https://kenbun.app', ))
    """

    url: AnyHttpUrl


class Blob(BaseModel):
    """
    >>> from unittest.mock import patch
    >>> with patch.object(Blob.__fields__["id"], "default_factory", return_value=Id("XsSoTH9cQzyT1xVxxxctNg")):
    ...     Blob(data=b"hello world", mime_type="text/plain")
    ...
    Blob(id=Id('XsSoTH9cQzyT1xVxxxctNg'), data=b'hello world', mime_type=<MimeType.text_plain: 'text/plain'>)
    """

    data: bytes
    mime_type: MimeType
