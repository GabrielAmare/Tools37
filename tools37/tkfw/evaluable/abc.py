from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

__all__ = [
    'Evaluable',
    'EvaluableGetter',
    'EvaluableSetter',
    'EvaluableBinder',
    'EvaluableExpression',
    'EvaluablePath',
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


class EvaluableExpression(Evaluable, ABC):
    """Super class for evaluable expressions."""

    @abstractmethod
    def get_paths(self) -> List[EvaluablePath]:
        """"""


class EvaluablePath(EvaluableBinder, EvaluableExpression, ABC):
    """"""
