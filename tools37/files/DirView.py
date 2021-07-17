from __future__ import annotations

import os
from abc import ABC
from typing import List, Type, TypeVar

from .DictInterface import DictInterface
from .FileView import FileView
from .JsonFileView import JsonFileView
from .PathView import PathView


class BaseDirView(PathView, ABC):
    def __init__(self, path: str):
        super().__init__(path)

        self.file_views: List[FileView] = []
        self.dir_views: List[DirView] = []

    def save(self) -> None:
        for file_view in self.file_views:
            file_view.save()

        for dir_view in self.dir_views:
            dir_view.save()

    def sub_path(self, name: str) -> str:
        return os.path.join(self.path, name)


J = TypeVar('J', bound=DictInterface)
D = TypeVar('D', bound=BaseDirView)


class DirView(BaseDirView, ABC):
    def load_json_file(self, name: str, factory: Type[J]) -> J:
        path = self.sub_path(name)
        file_view = JsonFileView(path, factory)
        file_view.load()
        self.file_views.append(file_view)
        return file_view.resource

    def load_dir(self, name: str, factory: Type[D]) -> D:
        path = self.sub_path(name)
        dir_view = factory(path)
        dir_view.load()
        self.dir_views.append(dir_view)
        return dir_view
