from __future__ import annotations

from typing import Optional

from .base import DynamicDict
from ..evaluable import as_evaluable_text

__all__ = ['DynamicStyle']


class DynamicStyle(DynamicDict):
    """
        DynamicDict with optional inheritance.
        - doesn't allow to set parent properties.
        - parse str values to DynamicTextModel if possible.
    """

    def __init__(self, style: dict = None, parent_style: DynamicStyle = None):
        self.parent_style: Optional[DynamicStyle] = parent_style
        DynamicDict.__init__(self, style)

    def __setitem__(self, key, value):
        if isinstance(value, str):
            value = as_evaluable_text(string=value)

        DynamicDict.__setitem__(self, key, value)

    def __getitem__(self, key):
        if DynamicDict.__contains__(self, key):
            return DynamicDict.__getitem__(self, key)

        elif self.parent_style:
            return self.parent_style[key]

        else:
            raise KeyError(key)

    def view(self) -> dict:
        style = {}

        if self.parent_style:
            style.update(self.parent_style.view())

        style.update(DynamicDict.view(self))

        return style
