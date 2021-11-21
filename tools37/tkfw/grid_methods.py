from tkinter import Grid
from typing import List

from .core_utils import Fill

__all__ = [
    'grid_centered_horizontally',
    'grid_centered_vertically',
    'grid_horizontally',
    'grid_vertically'
]


def _get_weights(widgets: List[Grid]) -> List[int]:
    return [1 if isinstance(widget, Fill) else 0 for widget in widgets]


def _grid_weights(parent: Grid, row_weights: List[int], column_weights: List[int]) -> None:
    for index, weight in enumerate(row_weights):
        parent.rowconfigure(index, weight=weight)

    for index, weight in enumerate(column_weights):
        parent.columnconfigure(index, weight=weight)


def grid_horizontally(parent: Grid, widgets: List[Grid], config: dict = None) -> None:
    _grid_weights(parent, [1], _get_weights(widgets))

    for index, widget in enumerate(widgets):
        widget.grid(row=0, column=index, **config)


def grid_centered_horizontally(parent: Grid, widgets: List[Grid], config: dict) -> None:
    _grid_weights(parent, [1, 0, 1], [1] + _get_weights(widgets) + [1])

    for index, widget in enumerate(widgets):
        widget.grid(row=1, column=index + 1, **config)


def grid_vertically(parent: Grid, widgets: List[Grid], config: dict = None) -> None:
    _grid_weights(parent, _get_weights(widgets), [1])

    for index, widget in enumerate(widgets):
        widget.grid(row=index, column=0, **config)


def grid_centered_vertically(parent: Grid, widgets: List[Grid], config: dict) -> None:
    _grid_weights(parent, [1] + _get_weights(widgets) + [1], [1, 0, 1])

    for index, widget in enumerate(widgets):
        widget.grid(row=index + 1, column=1, **config)
