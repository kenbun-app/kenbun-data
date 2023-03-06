from pydantic import BaseModel as _BaseModel
from pydantic import Field

from .fields import Id
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
        alias_generator = Camelizer(["url", "ip"])
        allow_population_by_field_name = True
