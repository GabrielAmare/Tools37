from __future__ import annotations

from typing import Optional

from .base import DynamicDict

__all__ = ['DynamicData']


class DynamicData(DynamicDict):
    """
        DynamicDict with optional inheritance.
        - allow to set parent item, if local data doesn't already contains the key.
    """

    def __init__(self, data: dict = None, parent_data: DynamicData = None):
        self.parent_data: Optional[DynamicData] = parent_data
        DynamicDict.__init__(self, data)

    def __setitem__(self, key, value):
        if self.parent_data and key in self.parent_data and not DynamicDict.__contains__(self, key):
            self.parent_data[key] = value

        else:
            DynamicDict.__setitem__(self, key, value)

    def __getitem__(self, key):
        if DynamicDict.__contains__(self, key):
            return DynamicDict.__getitem__(self, key)

        elif self.parent_data:
            return self.parent_data[key]

        else:
            raise KeyError(key)

    def view(self) -> dict:
        data = {}

        if self.parent_data:
            data.update(self.parent_data.view())

        data.update(super().view())

        return data
