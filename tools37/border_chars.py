CHARS = {
    "NNNN": " ",
    "NNSS": "─",
    "NNBB": "━",
    "SSNN": "│",
    "BBNN": "┃",
    "NNSS3": "┄",
    "NNBB3": "┅",
    "SSNN3": "┆",
    "BBNN3": "┇",
    "NNSS4": "┈",
    "NNBB4": "┉",
    "SSNN4": "┊",
    "BBNN4": "┋",
    "NSNS": "┌",
    "NSNB": "┍",
    "NBNS": "┎",
    "NBNB": "┏",
    "NSSN": "┐",
    "NSBN": "┑",
    "NBSN": "┒",
    "NBBN": "┓",
    "SNNS": "└",
    "SNNB": "┕",
    "BNNS": "┖",
    "BNNB": "┗",
    "SNSN": "┘",
    "SNBN": "┙",
    "BNSN": "┚",
    "BNBN": "┛",
    "SSNS": "├",
    "SSNB": "┝",
    "BSNS": "┞",
    "SBNS": "┟",
    "BBNS": "┠",
    "BSNB": "┡",
    "SBNB": "┢",
    "BBNB": "┣",
    "SSSN": "┤",
    "SSBN": "┥",
    "BSSN": "┦",
    "SBSN": "┧",
    "BBSN": "┨",
    "BSBN": "┩",
    "SBBN": "┪",
    "BBBN": "┫",
    "NSSS": "┬",
    "NSBS": "┭",
    "NSSB": "┮",
    "NSBB": "┯",
    "NBSS": "┰",
    "NBBS": "┱",
    "NBSB": "┲",
    "NBBB": "┳",
    "SNSS": "┴",
    "SNBS": "┵",
    "SNSB": "┶",
    "SNBB": "┷",
    "BNSS": "┸",
    "BNBS": "┹",
    "BNSB": "┺",
    "BNBB": "┻",
    "SSSS": "┼",
    "SSBS": "┽",
    "SSSB": "┾",
    "SSBB": "┿",
    "BSSS": "╀",
    "SBSS": "╁",
    "BBSS": "╂",
    "BSBS": "╃",
    "BSSB": "╄",
    "SBBS": "╅",
    "SBSB": "╆",
    "BSBB": "╇",
    "SBBB": "╈",
    "BBBS": "╉",
    "BBSB": "╊",
    "BBBB": "╋",
    "NNSS2": "╌",
    "NNBB2": "╍",
    "SSNN2": "╎",
    "BBNN2": "╏",
    "NNDD": "═",
    "DDNN": "║",
    "NSND": "╒",
    "NDNS": "╓",
    "NDND": "╔",
    "NSDN": "╕",
    "NDSN": "╖",
    "NDDN": "╗",
    "SNND": "╘",
    "DNNS": "╙",
    "DNND": "╚",
    "SNDN": "╛",
    "DNSN": "╜",
    "DNDN": "╝",
    "SSND": "╞",
    "DDNS": "╟",
    "DDND": "╠",
    "SSDN": "╡",
    "DDSN": "╢",
    "DDDN": "╣",
    "NSDD": "╤",
    "NDSS": "╥",
    "NDDD": "╦",
    "SNDD": "╧",
    "DNSS": "╨",
    "DNDD": "╩",
    "SSDD": "╪",
    "DDSS": "╫",
    "DDDD": "╬",
    "NNSN": "╴",
    "SNNN": "╵",
    "NNNS": "╶",
    "NSNN": "╷",
    "NNBN": "╸",
    "BNNN": "╹",
    "NNNB": "╺",
    "NBNN": "╻",
    "NNSB": "╼",
    "SBNN": "╽",
    "NNBS": "╾",
    "BSNN": "╿",
    "NSNSR": "╭",
    "NSSNR": "╮",
    "SNSNR": "╯",
    "SNNSR": "╰"
}


def _getseq():
    print(''.join(key[0] for key in CHARS.keys()))
    print(''.join(key[1] for key in CHARS.keys()))
    print(''.join(key[2] for key in CHARS.keys()))
    print(''.join(key[3] for key in CHARS.keys()))

    """
    NNSB NNSB NNSB NNNN NNNN SSBB SSBB SSBS BBSB SSBS BBSB NNNN NNNN SSSS BBBB SSSS BSBB BSSB SBBB NNSB NDNN NNNN SDDS DDSD DSDD NNNS DDSD DNSN NNBN NNSN B
    NNSB NNSB NNSB SSBB SSBB NNNN NNNN SSSB BSBB SSSB BSBB SSSS BBBB NNNN NNNN SSSS SBBS SBBS BBBB NNSB NDSD DSDD NNNN NNSD DSDD SDDN NNSD DNNN SNNN BNBN S
    SBNN SBNN SBNN NNNN SBSB NNNN SBSB NNNN NNNN SBSS SBBB SBSB SBSB SBSB SBSB SBSB SSSB SBSB BBSB SBNN DNNN NDSD NNND SDNN NDSD DSDD SDDS DSNN NBNN NSNB N
    SBNN SBNN SBNN SBSB NNNN SBSB NNNN SBSS SBBB NNNN NNNN SSBB SSBB SSBB SSBB SSBB SSSS BSBB BSBB SBNN DNDS DNNN DSDN NNDS DNNN DSDD SDDS DNNS NNNB NBNS N
    """


def _listall():
    s1 = range(ord('─'), ord('╬') + 1)
    s2 = range(ord('╴'), ord('╿') + 1)

    chars = ''.join(chr(i) for i in (*s1, *s2))
    print(repr(chars))

    with open('border_chars.json', mode='w', encoding='utf-8') as file:
        file.write('{')
        for key, val in CHARS.items():
            file.write(f'    "{key}": "{val}",')

        rchars = [char for char in chars if char not in CHARS.values()]

        for index, char in enumerate(rchars):
            sign = input(f"{index + 1}/{len(rchars)} sign of [{ord(char)}]{repr(char)} for NSEW : ")
            if sign:
                file.write(f'    "{sign}": "{char}",')
            else:
                break
        file.write('}')
