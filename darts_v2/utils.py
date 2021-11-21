from typing import ClassVar, Tuple, Type


class FontClass:
    XXS: ClassVar[Tuple[str, int]]
    XS: ClassVar[Tuple[str, int]]
    S: ClassVar[Tuple[str, int]]
    M: ClassVar[Tuple[str, int]]
    L: ClassVar[Tuple[str, int]]
    XL: ClassVar[Tuple[str, int]]
    XXL: ClassVar[Tuple[str, int]]


def linear_font(family: str, xxs: int, delta: int) -> Type[FontClass]:
    assert xxs >= 1

    class NewFontClass(FontClass):
        XXS = (family, xxs + delta * 0)
        XS = (family, xxs + delta * 1)
        S = (family, xxs + delta * 2)
        M = (family, xxs + delta * 3)
        L = (family, xxs + delta * 4)
        XL = (family, xxs + delta * 5)
        XXL = (family, xxs + delta * 6)

    return NewFontClass


def exp_font(family: str, xxs: int, factor: float) -> Type[FontClass]:
    assert xxs >= 1

    class NewFontClass(FontClass):
        XXS = (family, int(xxs * factor ** 0))
        XS = (family, int(xxs * factor ** 1))
        S = (family, int(xxs * factor ** 2))
        M = (family, int(xxs * factor ** 3))
        L = (family, int(xxs * factor ** 4))
        XL = (family, int(xxs * factor ** 5))
        XXL = (family, int(xxs * factor ** 6))

    return NewFontClass
