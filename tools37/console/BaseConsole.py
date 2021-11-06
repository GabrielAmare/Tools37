from tools37.text import Style, Overflow, Justify, Align
from typing import List
from tools37.colors import BLACK, GRAY, WHITE


class BaseConsole:
    DEFAULT_STYLE = Style(bg=BLACK, fg=WHITE)

    STYLES = {}
    ALIGNS = {}
    JUSTIFIES = {}
    OVERFLOWS = {}

    def __init__(self,
                 widths: List[int],
                 separator: str = ' █ ',
                 prefix: str = '█ ',
                 suffix: str = ' █',
                 border_style: Style = Style(bg=BLACK, fg=GRAY)
                 ):
        self.widths: List[int] = widths
        self.separator: str = separator
        self.prefix: str = prefix
        self.suffix: str = suffix
        self.border_style: Style = border_style

    def get_style(self, index: int, label: str) -> Style:
        for key in [(index, label), label, index]:
            try:
                return self.STYLES[key]

            except KeyError:
                continue

        else:
            return self.DEFAULT_STYLE

    def get_overflow(self, index: int, label: str) -> Overflow:
        for key in [(index, label), label, index]:
            try:
                return self.OVERFLOWS[key]

            except KeyError:
                continue

        else:
            return Overflow.ELLIPSIS

    def get_justify(self, index: int, label: str) -> Justify:
        for key in [(index, label), label, index]:
            try:
                return self.JUSTIFIES[key]

            except KeyError:
                continue

        else:
            return Justify.LEFT

    def get_align(self, index: int, label: str) -> Align:
        for key in [(index, label), label, index]:
            try:
                return self.ALIGNS[key]

            except KeyError:
                continue

        else:
            return Align.TOP

    def get_width(self, index: int):
        return self.widths[index]

    def display(self, *objects: object, label: str = '') -> None:
        data = [str(o).split('\n') for o in objects]

        for index, lines in enumerate(data):
            overflow = self.get_overflow(index, label)
            width = self.get_width(index)
            data[index] = overflow(lines, width)

        for index, lines in enumerate(data):
            justify = self.get_justify(index, label)
            width = self.get_width(index)
            data[index] = justify(lines, width, fill=' ')

        height = max(map(len, data))

        for index, lines in enumerate(data):
            align = self.get_align(index, label)
            width = self.get_width(index)
            data[index] = align(lines, width, height, fill=' ')

        for index, lines in enumerate(data):
            style = self.get_style(index, label)
            data[index] = list(map(style, lines))

        prefix = self.border_style(self.prefix)
        suffix = self.border_style(self.suffix)
        separator = self.border_style(self.separator)

        for row in zip(*data):
            print(prefix + separator.join(row) + suffix)
