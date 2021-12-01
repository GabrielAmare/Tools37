from abc import ABC, abstractmethod

__all__ = [
    'Code',
    'Object',
    'Expression'
]


class Code(ABC):
    @abstractmethod
    def __str__(self):
        """"""


class Object(Code, ABC):
    ...


class Expression(Object, ABC):
    ...
