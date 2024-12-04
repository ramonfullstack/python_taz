from abc import ABCMeta, abstractmethod
from typing import Any


class BaseLayer(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass
