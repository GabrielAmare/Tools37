from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Optional, Tuple, Generic, Callable, List, Iterator

__all__ = ['AbstractQuery', 'MapQuery', 'FilterQuery', 'Query']

E = TypeVar('E')
F = TypeVar('F')


class AbstractQuery(Generic[E], ABC):
    @abstractmethod
    def __iter__(self) -> Iterator[E]:
        """"""

    def map(self, function: Callable[[E], F]) -> MapQuery[E, F]:
        return MapQuery(self, function)

    def filter(self, function: Callable[[E], bool]) -> FilterQuery[E]:
        return FilterQuery(self, function)

    def starmap(self, function: Callable[[E, ...], F]) -> AbstractQuery[F]:
        return self.map(lambda item: function(*item))

    def where(self, **config) -> AbstractQuery[E]:
        return self.filter(lambda item: all(getattr(item, key) == val for key, val in config.items()))

    def getattr(self, key: str) -> AbstractQuery[E]:
        return self.map(lambda item: getattr(item, key))

    def getitem(self, key: object) -> AbstractQuery[E]:
        return self.map(lambda item: item[key])

    def first(self) -> Optional[E]:
        for item in self:
            return item

    def list(self) -> List[E]:
        return list(self)

    def tuple(self) -> Tuple[E]:
        return tuple(self)


class Query(Generic[E], AbstractQuery[E]):
    def __init__(self, data: List[E] = None):
        if data is None:
            data = []
        self.data: List[E] = data

    def __iter__(self) -> Iterator[E]:
        yield from self.data

    def append(self, item: E) -> None:
        self.data.append(item)

    def remove(self, item: E) -> None:
        self.data.remove(item)

    def insert(self, index: int, item: E) -> None:
        self.data.insert(index, item)


class FilterQuery(Generic[E], AbstractQuery[E]):
    def __init__(self, query: AbstractQuery[E], function: Callable[[E], bool]):
        self.query: AbstractQuery[E] = query
        self.function: Callable[[E], bool] = function

    def __iter__(self) -> Iterator[F]:
        for item in self.query:
            if self.function(item):
                yield item


class MapQuery(Generic[E, F], AbstractQuery[F]):
    def __init__(self, query: AbstractQuery[E], function: Callable[[E], F]):
        self.query: AbstractQuery[E] = query
        self.function: Callable[[E], F] = function

    def __iter__(self) -> Iterator[F]:
        for item in self.query:
            yield self.function(item)
