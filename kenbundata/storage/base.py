from abc import ABCMeta, abstractmethod

from ..fields import Id
from ..types import Url


class BaseStorage(metaclass=ABCMeta):
    @abstractmethod
    def get_url_by_id(self, id: Id) -> Url:
        raise NotImplementedError

    @abstractmethod
    def store_url(self, url: Url) -> None:
        raise NotImplementedError
