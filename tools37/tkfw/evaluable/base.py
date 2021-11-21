from abc import ABC
from dataclasses import dataclass, replace
from typing import List, Any, Type

from . import abc

__all__ = [
    'EvaluateGetter',
    'EvaluableDictItem',
    'EvaluableListItem',
    'EvaluablePath',
    'EvaluableText'
]


class EvaluateGetter(abc.EvaluableGetter, ABC):
    def evaluate(self, data: Any) -> Any:
        return self.get(data)


def _check_data_type(data: Any, type_: Type) -> None:
    if not isinstance(data, type_):
        raise TypeError(f"{data} should be {type_.__name__}.")


@dataclass
class EvaluableDictItem(EvaluateGetter, abc.EvaluableBinder):
    key: str

    def __str__(self):
        return f"{self.key!s}"

    @classmethod
    def _check_data_type(cls, data):
        if not isinstance(data, dict):
            raise TypeError(f"{data} should be dict.")

    def get(self, data: Any) -> Any:
        _check_data_type(data, dict)
        return data[self.key]

    def set(self, data: Any, value: Any) -> None:
        _check_data_type(data, dict)
        data[self.key] = value


@dataclass
class EvaluableListItem(EvaluateGetter, abc.EvaluableBinder):
    index: int

    def __str__(self):
        return f"{self.index!s}"

    def get(self, data: Any) -> Any:
        _check_data_type(data, list)
        return data[self.index]

    def set(self, data: Any, value: Any) -> None:
        _check_data_type(data, list)
        data[self.index] = value


@dataclass
class EvaluablePath(EvaluateGetter, abc.EvaluablePath):
    steps: List[abc.EvaluableBinder]

    def __str__(self):
        return ".".join(map(str, self.steps))

    def _get_partial_path(self, index: int) -> str:
        return '.'.join(map(str, self.steps[:index + 1]))

    def _get_type_error(self, index: int, data: Any) -> TypeError:
        return TypeError(f"the data at {self._get_partial_path(index)} has the wrong type.\n"
                         f"data = {data!r}")

    def get(self, data: Any) -> Any:
        for index, step in enumerate(self.steps):
            try:
                data = step.get(data)

            except TypeError as error:
                raise self._get_type_error(index, data) from error

        return data

    def set(self, data: Any, value: Any) -> None:
        for step in self.steps[:-1]:
            data = step.get(data)

        self.steps[-1].set(data, value)

    def __add__(self, other: 'EvaluablePath') -> 'EvaluablePath':
        return replace(self, steps=self.steps + other.steps)

    def get_paths(self) -> List[abc.EvaluablePath]:
        return [self]


@dataclass
class EvaluableText(abc.Evaluable):
    expression: str
    values: List[abc.Evaluable]

    def evaluate(self, data: Any):
        values = [value.evaluate(data) for value in self.values]
        return self.expression.format(*map(str, values))

    def __str__(self):
        return self.expression.format(*map(str, self.values))
