from typing import Dict

from tools37.colors import hex_to_rgb


class _AnsiColor:
    def __init__(self, raw: Dict[str, str], rgb: str):
        self.raw: Dict[str, str] = raw
        self.rgb: str = rgb

    def __call__(self, code: str) -> str:
        """Convert color `name` | `hexadecimal code` into ANSI color code"""
        try:
            return self.raw[code]

        except KeyError:
            return self.rgb % hex_to_rgb(code)


class ANSI:
    DEFAULT = '\33[0m'
    BOLD = '\33[1m'
    FAINT = '\33[2m'
    ITALIC = '\33[3m'
    UNDERLINE = '\33[4m'
    BLINK_SLOW = '\33[5m'
    BLINK_FAST = '\33[6m'
    REVERSE = '\33[7m'  # switch foreground & background colors
    CONCEAL = '\33[8m'
    CROSS_LINE = '\33[9m'

    COLORS = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

    FOREGROUND = _AnsiColor({
        "black": '\33[30m',
        "red": '\33[31m',
        "green": '\33[32m',
        "yellow": '\33[33m',
        "blue": '\33[34m',
        "magenta": '\33[35m',
        "cyan": '\33[36m',
        "white": '\33[37m'
    }, f"\033[38;2;%s;%s;%sm")
    BACKGROUND = _AnsiColor({
        "black": '\33[40m',
        "red": '\33[41m',
        "green": '\33[42m',
        "yellow": '\33[43m',
        "blue": '\33[44m',
        "magenta": '\33[45m',
        "cyan": '\33[46m',
        "white": '\33[47m',
    }, f"\033[48;2;%s;%s;%sm")

    class CURSOR:
        UP = '\33[%sA'
        DOWN = '\33[%sB'
        RIGHT = '\33[%sC'
        LEFT = '\33[%sD'
        TO = '\33[{row};{col}H'

        CLS = '\33[2J'  # cls ???
        SAVE = '\33[s'
        LOAD = '\33[u'
        HIDE = '\33[?25l'
        SHOW = '\33[?25h'
        TRIM_OFF_LINE = '\33[K'  # trim off line from curser position
