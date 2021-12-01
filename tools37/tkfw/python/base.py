from abc import ABC
from dataclasses import dataclass
from typing import Union, List

from .abc import Code, Object, Expression

__all__ = [
    'Variable',
    'Int',
    'Float',
    'Str',
    'GetItem',
    'GetAttr',
    'AsArgs',
    'AsKwargs',
    'Arg',
    'Kwarg',
    'Arguments',
    'Call',
    'Assign',
    'UnaryOperator',
    'BinaryOperator',
    'SetItem',
    'SetAttr'
]


@dataclass
class Variable(Code):
    name: str

    def __str__(self):
        return str(self.name)


@dataclass
class Int(Object):
    value: int

    def __str__(self):
        return repr(self.value)


@dataclass
class Float(Object):
    value: float

    def __str__(self):
        return repr(self.value)


@dataclass
class Str(Object):
    content: str

    def __str__(self):
        return repr(self.content)


@dataclass
class GetItem(Object):
    base: Object
    item: Code

    def __str__(self):
        return f"{self.base!s}[{self.item!s}]"


@dataclass
class GetAttr(Object):
    base: Object
    name: Variable

    def __str__(self):
        return f"{self.base!s}.{self.name!s}"


@dataclass
class AsArgs(Code):
    base: Object

    def __str__(self):
        return f"*{self.base!s}"


@dataclass
class AsKwargs(Code):
    base: Object

    def __str__(self):
        return f"**{self.base!s}"


@dataclass
class Arg(Code):
    value: Object

    def __str__(self):
        return str(self.value)


@dataclass
class Kwarg(Code):
    name: Variable
    value: Object

    def __str__(self):
        return f"{self.name!s}={self.value!s}"


@dataclass
class Arguments:
    args: List[Union[Arg, AsArgs]]
    kwargs: List[Union[Kwarg, AsKwargs]]

    def __str__(self):
        return ', '.join(map(str, [*self.args, *self.kwargs]))


@dataclass
class Call(Object):
    base: Object
    args: Arguments

    def __str__(self):
        return f"{self.base!s}({self.args!s})"


@dataclass
class Assign(Code):
    base: Union[Variable, GetItem, GetAttr]
    value: Object

    def __str__(self):
        return f"{self.base!s} = {self.value!s}"


@dataclass
class UnaryOperator(Expression, ABC):
    right: Object


@dataclass
class BinaryOperator(Expression, ABC):
    left: Object
    right: Object


def SetItem(base, item, value):
    return Assign(base=GetItem(base, item), value=value)


def SetAttr(base, name, value):
    return Assign(base=GetAttr(base, name), value=value)
