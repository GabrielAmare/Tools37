from abc import ABC, abstractmethod
from typing import Type, TypeVar

from tools37.files import JsonFile

E = TypeVar('E')


class ListInterface(ABC):
    @classmethod
    @abstractmethod
    def from_list(cls: Type[E], data: list) -> E:
        """"""

    @abstractmethod
    def to_list(self) -> list:
        """"""


class DictInterface(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls: Type[E], data: dict) -> E:
        """"""

    @abstractmethod
    def to_dict(self) -> dict:
        """"""


class JsonInterface(ABC):
    @classmethod
    @abstractmethod
    def load(cls: Type[E], fp: str) -> E:
        """"""

    @abstractmethod
    def save(self, fp: str) -> None:
        """"""


class JsonDictInterface(JsonInterface, DictInterface, ABC):
    @classmethod
    def load(cls: Type[E], fp: str) -> E:
        data = JsonFile.load(fp)
        return cls.from_dict(data)

    def save(self, fp: str) -> None:
        data = self.to_dict()
        JsonFile.save(fp, data)


class JsonListInterface(JsonInterface, ListInterface, ABC):
    @classmethod
    def load(cls: Type[E], fp: str) -> E:
        data = JsonFile.load(fp)
        return cls.from_list(data)

    def save(self, fp: str) -> None:
        data = self.to_list()
        JsonFile.save(fp, data)
