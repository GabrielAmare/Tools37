from typing import List

__all__ = ["ReprTable"]


class ReprTable:
    SIMPLE = '┌┬─┐├┼─┤││ │└┴─┘'
    DOUBLE = '╔╦═╗╠╬═╣║║ ║╚╩═╝'
    DV_SH = '╓╥─╖╟╫─╢║║ ║╙╨─╜'
    DH_SV = '╒╤═╕╞╪═╡││ │╘╧═╛'
    BOLD = '┏┳━┓┣╋━┫┃┃ ┃┗┻━┛'

    def __init__(self, data: List[List[str]], padx: int = 1, pady: int = 0, chart: str = BOLD):
        self.data: List[List[str]] = data
        self.padx: int = padx
        self.pady: int = pady

        self.chart: str = chart
        self.widths: List[int] = [
            max([
                max([
                    len(line) for line in cell.split('\n')
                ], default=0)
                for cell in col
            ], default=0)
            for col in zip(*self.data)
        ]
        self.heights: List[int] = [
            max([
                len(cell.split('\n'))
                for cell in row
            ], default=0)
            for row in self.data
        ]

    def get_box(self, text: str, width: int, height: int) -> List[str]:
        lines = text.split('\n')
        empty = width * self.chart[10]
        lines.extend((height - len(lines)) * [empty])
        return self.pady * [empty] + [
            self.padx * self.chart[10] + line.ljust(width, self.chart[10]) + self.padx * self.chart[10]
            for line in lines
        ] + self.pady * [empty]

    def __str__(self):
        start_line = self.chart[0] + self.chart[1].join(
            (width + 2 * self.padx) * self.chart[2]
            for width in self.widths
        ) + self.chart[3]
        sep_line = self.chart[4] + self.chart[5].join(
            (width + 2 * self.padx) * self.chart[6]
            for width in self.widths
        ) + self.chart[7]
        end_line = self.chart[12] + self.chart[13].join(
            (width + 2 * self.padx) * self.chart[14]
            for width in self.widths
        ) + self.chart[15]

        return '\n'.join([
            start_line,
            ('\n' + sep_line + '\n').join(
                '\n'.join(
                    self.chart[8] + self.chart[9].join(
                        text.ljust((width + 2 * self.padx), self.chart[10])
                        for width, text in zip(self.widths, nrow)
                    ) + self.chart[11]
                    for nrow in zip(*(
                        self.get_box(text, width, height)
                        for text, width in zip(row, self.widths)
                    ))
                )
                for row, height in zip(self.data, self.heights)
            ),
            end_line
        ])


if __name__ == '__main__':
    data = [
        ["first name", "last name", "deceased"],
        ["Barack", "Obama", "N"],
        ["Joe", "Biden", "N"],
        ["Michael", "Jackson", "Y"],
        ["John", "Doe", "?"],
        ["John", "Fitzgerald\nKennedy", "Y"],
        ["Someone", "-/-", "-/-"],
    ]

    table = ReprTable(data)

    print(table)
