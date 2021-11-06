from enum import Enum
from typing import List


def _justify_left(lines: List[str], width: int, fill: str = ' ') -> List[str]:
    return [line.ljust(width, fill) for line in lines]


def _justify_right(lines: List[str], width: int, fill: str = ' ') -> List[str]:
    return [line.rjust(width, fill) for line in lines]


def _justify_center(lines: List[str], width: int, fill: str = ' ') -> List[str]:
    return [line.center(width, fill) for line in lines]


def _justify_spaced(lines: List[str], width: int, fill: str = ' ') -> List[str]:
    result = []
    for line in lines:
        if len(line) < width:
            words = [word for word in line.split(fill) if word]

            if len(words) == 0:
                line = fill * width

            elif len(words) == 1:
                line = words[0].ljust(width, fill)

            else:
                remain = width - sum(map(len, words)) - (len(words) - 1)

                index = 0
                while remain:
                    words[index % (len(words) - 1)] += fill
                    remain -= 1
                    index += 1

                line = fill.join(words)

        result.append(line)

    return result


class Justify(Enum):
    LEFT = _justify_left
    RIGHT = _justify_right
    CENTER = _justify_center
    SPACED = _justify_spaced

    def __call__(self, lines: List[str], width: int, fill: str = ' ') -> List[str]:
        raise ValueError(f"Invalid {self.__class__.__name__} tag : {self}")
