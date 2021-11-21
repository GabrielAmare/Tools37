from enum import Enum

from .utils import linear_font, exp_font

Font = exp_font(family='Terminal', xxs=5, factor=1.4)
Icon = linear_font(family='HoloLens MDL2 Assets', xxs=6, delta=1)


class Border(dict, Enum):
    NULL = dict(bd=0, relief="flat")
    BUTTON = dict(bd=6, relief="raised")
    ENTRY = dict(bd=6, relief="sunken")
    BOX = dict(bd=6, relief="ridge")


class Color(dict, Enum):
    DARK = dict(background='#080705', foreground='#FDFDFD', insertbackground='#FDFDFD')
    DARK_ERROR = dict(background='#080705', foreground='red', insertbackground='#FDFDFD')

    LIGHT = dict(background='#FDE7C2', foreground='#020202', insertbackground='#020202')
    LIGHT_ERROR = dict(background='#FDE7C2', foreground='red', insertbackground='#020202')

    CLICKABLE = dict(
        background='#088937', foreground='#00041f',
        activebackground='#00b000', activeforeground='#00041f',
        disabledforeground='#400f05',
    )
    CLICKABLE2 = dict(
        background='#ED333E', foreground='#00041f',
        activebackground='#00b000', activeforeground='#00041f',
        disabledforeground='#400f05',
    )


class Padding(dict, Enum):
    NULL = dict(padx=0, pady=0)
    XXS = dict(padx=1, pady=1)
    XS = dict(padx=2, pady=2)
    S = dict(padx=3, pady=3)
    M = dict(padx=4, pady=4)
    L = dict(padx=5, pady=5)
    XL = dict(padx=6, pady=6)
    XXL = dict(padx=7, pady=7)


def style(color: Color, border: Border = None, padding: Padding = None, **config):
    if border is None:
        border = Border.NULL

    if padding is None:
        padding = Padding.NULL

    return {
        **color,
        **border,
        **padding,
        **config
    }


button_style = dict(anchor="center", cursor='hand2')

AVAILABLE_GAMES = ['301', '501', '801']
