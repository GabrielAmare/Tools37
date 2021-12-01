from tkinter import Grid
from typing import List

from .abc import Component, GridMethod
from .utils import Fill

__all__ = [
    'GridHorizontally',
    'GridVertically',
    'GridCenteredHorizontally',
    'GridCenteredVertically'
]


def _get_weights(widgets: List[Grid]) -> List[int]:
    return [1 if isinstance(widget, Fill) else 0 for widget in widgets]


def _grid_weights(parent: Grid, row_weights: List[int], column_weights: List[int]) -> None:
    for index, weight in enumerate(row_weights):
        parent.rowconfigure(index, weight=weight)

    for index, weight in enumerate(column_weights):
        parent.columnconfigure(index, weight=weight)


class GridHorizontally(GridMethod):
    def __init__(self, config: dict):
        self.config: dict = config

    def __call__(self, parent: Component, widgets: List[Component]):
        _grid_weights(parent, [1], _get_weights(widgets))

        for index, widget in enumerate(widgets):
            widget.grid(row=0, column=index, **self.config)


class GridVertically(GridMethod):
    def __init__(self, config: dict):
        self.config: dict = config

    def __call__(self, parent: Component, widgets: List[Component]):
        _grid_weights(parent, _get_weights(widgets), [1])

        for index, widget in enumerate(widgets):
            widget.grid(row=index, column=0, **self.config)


class GridCenteredHorizontally(GridMethod):
    def __init__(self, config: dict):
        self.config: dict = config

    def __call__(self, parent: Component, widgets: List[Component]):
        _grid_weights(parent, [1, 0, 1], [1] + _get_weights(widgets) + [1])

        for index, widget in enumerate(widgets):
            widget.grid(row=1, column=index + 1, **self.config)


class GridCenteredVertically(GridMethod):
    def __init__(self, config: dict):
        self.config: dict = config

    def __call__(self, parent: Component, widgets: List[Component]):
        _grid_weights(parent, [1] + _get_weights(widgets) + [1], [1, 0, 1])

        for index, widget in enumerate(widgets):
            widget.grid(row=index + 1, column=1, **self.config)
