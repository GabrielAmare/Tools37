from numbers import Real

from .BoundingBox import BoundingBox


class AbsoluteBoundingBox(BoundingBox):
    def __init__(self, xi: Real, yi: Real, xf: Real, yf: Real):
        assert xi < xf
        assert yi < yf
        self.xi: Real = xi
        self.yi: Real = yi
        self.xf: Real = xf
        self.yf: Real = yf

    @property
    def x(self) -> Real:
        return (self.xi + self.xf) / 2

    @x.setter
    def x(self, value: Real):
        self.xi, self.xf = value - self.dx, value + self.dx

    @property
    def y(self) -> Real:
        return (self.xi + self.xf) / 2

    @y.setter
    def y(self, value: Real):
        self.yi, self.yf = value - self.dy, value + self.dy

    @property
    def dx(self) -> Real:
        return (self.xf - self.xi) / 2

    @dx.setter
    def dx(self, value: Real):
        self.xi, self.xf = self.x - value, self.x + value

    @property
    def dy(self) -> Real:
        return (self.yf - self.yi) / 2

    @dy.setter
    def dy(self, value: Real):
        self.yi, self.yf = self.y - value, self.y + value
