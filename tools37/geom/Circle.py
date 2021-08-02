from numbers import Real

from tools37.Typed import Typed, typedmethod
from .Coords import Coords


class Circle(Typed):
    def __init__(self, center: Coords, radius: Real):
        assert float(radius) > 0
        self.center: Coords = center
        self.radius: Real = radius

    def __repr__(self):
        return f"{self.__class__.__name__}({self.center!r}, {self.radius!r})"

    def __eq__(self, other):
        return type(self) is type(other) and self.center == other.center and self.radius == other.radius

    @typedmethod(Coords)
    def __contains__(self, other: Coords) -> bool:
        return abs(other - self.center) <= self.radius

    @typedmethod(Coords)
    def __lshift__(self, other: Coords) -> Coords:
        """Return the projection of other on the border of self."""
        return self.center + self.radius * (other - self.center).__unit__()

    @typedmethod(Coords)
    def __rrshift__(self, other: Coords) -> Coords:
        return self << other
