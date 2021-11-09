from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar

E = TypeVar('E')


class TableInterface(Generic[E], ABC):
    @abstractmethod
    def append_row(self, elements: List[E]) -> None:
        """"""

    @abstractmethod
    def remove_row(self, index: int) -> None:
        """"""

    @abstractmethod
    def insert_row(self, index: int, elements: List[E]) -> None:
        """"""

    @abstractmethod
    def set_row(self, index: int, elements: List[E]) -> None:
        """"""

    @abstractmethod
    def get_row(self, index: int) -> List[E]:
        """"""

    @abstractmethod
    def pop_row(self, index: int) -> List[E]:
        """"""

    @abstractmethod
    def append_col(self, elements: List[E]) -> None:
        """"""

    @abstractmethod
    def remove_col(self, index: int) -> None:
        """"""

    @abstractmethod
    def insert_col(self, index: int, elements: List[E]) -> None:
        """"""

    @abstractmethod
    def set_col(self, index: int, elements: List[E]) -> None:
        """"""

    @abstractmethod
    def get_col(self, index: int) -> List[E]:
        """"""

    @abstractmethod
    def pop_col(self, index: int) -> List[E]:
        """"""


class Table(Generic[E], TableInterface[E]):
    @classmethod
    def sized(cls, n_rows: int, n_cols: int, default: E = None):
        return cls([
            [
                default
                for i_col in range(n_cols)
            ]
            for i_row in range(n_rows)
        ])

    def __init__(self, data: List[List[E]]):
        assert len(set(map(len, data))) == 1
        self.data: List[List[E]] = data
        self.n_rows: int = len(data)
        self.n_cols: int = len(data[0])

    def append_row(self, elements: List[E]) -> None:
        assert len(elements) == self.n_cols
        self.data.append(elements)
        self.n_rows += 1

    def remove_row(self, index: int) -> None:
        del self.data[index]
        self.n_rows -= 1

    def insert_row(self, index: int, elements: List[E]) -> None:
        assert len(elements) == self.n_cols
        self.data.insert(index, elements)
        self.n_rows += 1

    def set_row(self, index: int, elements: List[E]) -> None:
        assert len(elements) == self.n_cols
        self.data[index] = elements

    def get_row(self, index: int) -> List[E]:
        return self.data[index]

    def pop_row(self, index: int) -> List[E]:
        elements = self.data.pop(index)
        self.n_rows -= 1
        return elements

    def append_col(self, elements: List[E]) -> None:
        assert len(elements) == self.n_rows
        for row, element in zip(self.data, elements):
            row.append(element)
        self.n_cols += 1

    def remove_col(self, index: int) -> None:
        for row in self.data:
            del row[index]

    def insert_col(self, index: int, elements: List[E]) -> None:
        assert len(elements) == self.n_rows
        for row, element in zip(self.data, elements):
            row.insert(index, element)
        self.n_cols += 1

    def set_col(self, index: int, elements: List[E]) -> None:
        assert len(elements) == self.n_rows
        for row, element in zip(self.data, elements):
            row[index] = element

    def get_col(self, index: int) -> List[E]:
        return [row[index] for row in self.data]

    def pop_col(self, index: int) -> List[E]:
        elements = [row.pop(index) for row in self.data]
        self.n_cols -= 1
        return elements
