from enum import Enum
from typing import List


def _overflow_wrap(lines: List[str], width: int) -> List[str]:
    result = []
    for line in lines:
        while len(line) > width:
            result.append(line[:width])
            line = line[width:]

        result.append(line)

    return result


def _overflow_cut(lines: List[str], width: int) -> List[str]:
    return [line[:width] for line in lines]


def _overflow_word_wrap(lines: List[str], width: int) -> List[str]:
    result = []
    for line in lines:
        curr = ''
        for word in line.split(' '):
            while len(curr) > width:
                result.append(curr[:width - 1] + '…')
                curr = '…' + curr[width - 1:]

            if len(curr) + len(word) + 1 > width:
                result.append(curr)
                curr = word

            elif curr:
                curr += ' ' + word

            else:
                curr = word
        if curr:
            result.append(curr)
    return result


def _overflow_ellispis(lines: List[str], width: int) -> List[str]:
    return [line if len(line) <= width else line[:width - 1] + '…' for line in lines]


class Overflow(Enum):
    CUT = _overflow_cut
    WRAP = _overflow_wrap
    ELLIPSIS = _overflow_ellispis
    WORD_WRAP = _overflow_word_wrap

    def __call__(self, lines: List[str], width: int) -> List[str]:
        raise ValueError(f"Invalid {self.__class__.__name__} tag : {self}")
