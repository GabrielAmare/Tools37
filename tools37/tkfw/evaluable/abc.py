from abc import ABC, abstractmethod
from typing import Any

__all__ = [
    'Evaluable',
    'EvaluableGetter',
    'EvaluableSetter',
    'EvaluableBinder'
]


class Evaluable(ABC):
    @abstractmethod
    def evaluate(self, data: Any):
        """"""

    @abstractmethod
    def __str__(self) -> str:
        """"""


class EvaluableGetter(Evaluable, ABC):
    @abstractmethod
    def get(self, data: Any) -> Any:
        """"""


class EvaluableSetter(Evaluable, ABC):
    @abstractmethod
    def set(self, data: Any, value: Any) -> None:
        """"""


class EvaluableBinder(EvaluableGetter, EvaluableSetter, ABC):
    """"""
