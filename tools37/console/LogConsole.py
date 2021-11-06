from datetime import datetime

from tools37.colors import BLACK, YELLOW, RED, GREEN
from tools37.text import Style, Overflow, Justify, Align
from .BaseConsole import BaseConsole


class LogConsole(BaseConsole):
    STYLES = {
        'SUCCESS': Style(bg=BLACK, fg=GREEN),
        'FAILURE': Style(bg=BLACK, fg=RED),
        'WARNING': Style(bg=BLACK, fg=YELLOW),
    }
    OVERFLOWS = {
        0: Overflow.ELLIPSIS,
        1: Overflow.CUT,
        2: Overflow.WORD_WRAP
    }
    JUSTIFIES = {
        0: Justify.LEFT,
        1: Justify.RIGHT,
        2: Justify.LEFT,
    }
    ALIGNS = {
        0: Align.TOP,
        1: Align.TOP,
        2: Align.TOP,
    }

    def __init__(self, width: int):
        labels_length = max(map(len, self.STYLES))
        assert width > 4 + 26 + labels_length
        super().__init__(widths=[26, labels_length, width - 3 - 26 - labels_length])

    def _print(self, label: str, *values: object):
        self.display(datetime.now(), label, *values, label=label)

    def print(self, *values: object):
        self._print('', *values)

    def success(self, *values: object):
        self._print('SUCCESS', *values)

    def failure(self, *values: object):
        self._print('FAILURE', *values)

    def warning(self, *values: object):
        self._print('WARNING', *values)
