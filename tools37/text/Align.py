from enum import Enum
from typing import List


def _align_top(lines: List[str], width: int, height: int, fill: str = ' ') -> List[str]:
    missing = height - len(lines)

    if missing <= 0:
        return lines

    return lines + missing * [width * fill]


def _align_bottom(lines: List[str], width: int, height: int, fill: str = ' ') -> List[str]:
    missing = height - len(lines)

    if missing <= 0:
        return lines

    return missing * [width * fill] + lines


def _align_middle(lines: List[str], width: int, height: int, fill: str = ' ') -> List[str]:
    missing = height - len(lines)

    if missing <= 0:
        return lines

    missing_top = missing // 2
    missing_bottom = missing - missing_top

    return missing_top * [width * fill] + lines + missing_bottom * [width * fill]


def _align_spaced(lines: List[str], width: int, height: int, fill: str = ' ') -> List[str]:
    raise NotImplementedError


class Align(Enum):
    TOP = _align_top
    BOTTOM = _align_bottom
    MIDDLE = _align_middle
    SPACED = _align_spaced

    def __call__(self, lines: List[str], width: int, height: int, fill: str = ' ') -> List[str]:
        raise ValueError(f"Invalid {self.__class__.__name__} tag : {self}")
