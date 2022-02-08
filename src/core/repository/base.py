from abc import ABC, abstractmethod
from typing import List, TypeVar

T = TypeVar("T")


class Repository(ABC):
    @abstractmethod
    def get(self, id: int) -> T:
        pass

    @abstractmethod
    def list(self) -> List[T]:
        pass

    @abstractmethod
    def filter(self, **kwargs) -> List[T]:
        pass
