from __future__ import annotations

from numbers import Real
from typing import TypeVar, Generator, Generic

from tools37.Typed import Typed, typedmethod, TypedArg

N = TypeVar('N', bound=Real)


class Vector(Generic[N], Typed):
    def __init__(self, x: N, y: N):
        self.x: N = x
        self.y: N = y

    def __iter__(self) -> Generator[N]:
        yield self.x
        yield self.y

    def __len__(self) -> int:
        return 2

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x!r}, {self.y!r})"

    def __eq__(self, other):
        return type(self) is type(other) and self.x == other.x and self.y == other.y

    def __getitem__(self, index: int) -> N:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError(index)

    def __setitem__(self, index: int, value: N) -> None:
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError(index)

    def __abs__(self) -> N:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    ####################################################################################################################
    # VECTOR x SCALAR operations
    ####################################################################################################################

    @typedmethod(Real)
    def __add__(self, other) -> Vector:
        return Vector(self.x + other, self.y + other)

    @typedmethod(Real)
    def __radd__(self, other) -> Vector:
        return Vector(other + self.x, other + self.y)

    @typedmethod(Real)
    def __sub__(self, other) -> Vector:
        return Vector(self.x - other, self.y - other)

    @typedmethod(Real)
    def __rsub__(self, other) -> Vector:
        return Vector(other - self.x, other - self.y)

    @typedmethod(Real)
    def __mul__(self, other) -> Vector:
        return Vector(self.x * other, self.y * other)

    @typedmethod(Real)
    def __rmul__(self, other) -> Vector:
        return Vector(other * self.x, other * self.y)

    @typedmethod(Real)
    def __truediv__(self, other) -> Vector:
        return Vector(self.x / other, self.y / other)

    ####################################################################################################################
    # VECTOR x VECTOR operations
    ####################################################################################################################

    @typedmethod(TypedArg.CLASS)
    def __add__(self, other) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    @typedmethod(TypedArg.CLASS)
    def __sub__(self, other) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    @typedmethod(TypedArg.CLASS)
    def __mul__(self, other) -> N:
        """Represent the inner product of two vectors."""
        return self.x * other.x + self.y * other.y

    @typedmethod(TypedArg.CLASS)
    def __xor__(self, other) -> N:
        """Represent the outer product of two vectors."""
        return self.x * other.y - self.y * other.x

    ####################################################################################################################
    # VECTOR x ??? operations -> NotImplemented
    ####################################################################################################################

    @typedmethod(object)
    def __add__(self, _):
        return NotImplemented

    @typedmethod(object)
    def __radd__(self, _):
        return NotImplemented

    @typedmethod(object)
    def __sub__(self, _):
        return NotImplemented

    @typedmethod(object)
    def __rsub__(self, _):
        return NotImplemented

    @typedmethod(object)
    def __mul__(self, _):
        return NotImplemented

    @typedmethod(object)
    def __rmul__(self, _):
        return NotImplemented

    @typedmethod(object)
    def __xor__(self, _):
        return NotImplemented

    @typedmethod(object)
    def __rxor__(self, _):
        return NotImplemented

    @typedmethod(object)
    def __truediv__(self, _):
        return NotImplemented

    @typedmethod(object)
    def __rtruediv__(self, _):
        return NotImplemented
