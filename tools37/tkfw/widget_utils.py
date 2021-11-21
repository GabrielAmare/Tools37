from .widgets import Frame
from .core_utils import Horizontal, Vertical, Fill


class Row(Frame, Horizontal):
    pass


class Column(Frame, Vertical):
    pass


class LargeRow(Frame, Horizontal, Fill):
    pass


class LargeColumn(Frame, Vertical, Fill):
    pass
