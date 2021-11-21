from ..core_utils import Horizontal, Vertical, Centered
from ..interfaces import Tree


class Leaf(Tree):
    """Tree which have no childs."""

    @classmethod
    def _init_grid_method(cls):
        if issubclass(cls, Horizontal):
            raise Exception(f"Leaf cannot implement Horizontal")

        if issubclass(cls, Vertical):
            raise Exception(f"Leaf cannot implement Vertical")

        if issubclass(cls, Centered):
            raise Exception(f"Leaf cannot implement Centered")

        cls._grid_method = None

    def grid_widgets(self, widgets):
        pass
