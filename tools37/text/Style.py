from dataclasses import dataclass

from tools37.colors import BLACK, WHITE
from .Ansi import ANSI


@dataclass
class Style:
    """This class can be use to style text with colors and effects."""
    bg: str = BLACK
    fg: str = WHITE

    bold: bool = False
    faint: bool = False
    italic: bool = False
    underline: bool = False
    blink_slow: bool = False
    blink_fast: bool = False
    reverse: bool = False
    conceal: bool = False
    cross_line: bool = False

    @property
    def prefix(self) -> str:
        prefix = ANSI.BACKGROUND(self.bg) + ANSI.FOREGROUND(self.fg)
        if self.bold:
            prefix += ANSI.BOLD
        if self.faint:
            prefix += ANSI.FAINT
        if self.italic:
            prefix += ANSI.ITALIC
        if self.underline:
            prefix += ANSI.UNDERLINE
        if self.blink_slow:
            prefix += ANSI.BLINK_SLOW
        if self.blink_fast:
            prefix += ANSI.BLINK_FAST
        if self.reverse:
            prefix += ANSI.REVERSE
        if self.conceal:
            prefix += ANSI.CONCEAL
        if self.cross_line:
            prefix += ANSI.CROSS_LINE
        return prefix

    def __call__(self, text: str) -> str:
        return self.prefix + text + ANSI.DEFAULT
