from abc import ABC
from typing import TypeVar, Type, Generic

from .DictInterface import DictInterface
from .FileView import FileView
from .JsonFile import JsonFile

E = TypeVar('E', bound=DictInterface)


class JsonFileView(FileView[E], Generic[E], ABC):
    def load(self) -> None:
        file_data = JsonFile.load(self.file_path)
        self.resource = self.factory.from_dict(file_data)

    def save(self) -> None:
        if isinstance(self.resource, self.factory):
            file_data = self.resource.to_dict()
            JsonFile.save(self.file_path, file_data)
