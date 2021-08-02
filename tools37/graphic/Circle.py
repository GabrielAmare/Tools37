from numbers import Real
from tkinter import Canvas

from tools37 import geom
from .GraphicShape import GraphicShape


class Circle(geom.Circle, GraphicShape):
    create_method = Canvas.create_oval

    def __init__(self, cnv: Canvas, center: geom.Coords, radius: Real, **config):
        geom.Circle.__init__(self, center, radius)
        GraphicShape.__init__(self, cnv, **config)

    def coords(self):
        return map(int, (*(self.center - self.radius), *(self.center + self.radius)))
