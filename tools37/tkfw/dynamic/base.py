from abc import ABC
from dataclasses import dataclass
from typing import List, Any

from . import abc
from ..evaluable import EvaluableListItem, EvaluableDictItem, EvaluablePath
from tools37.tkfw._commented.events import Emitter

__all__ = [
    'DynamicDict',  # overwrite abc
    'DynamicList',  # overwrite abc

    'DynamicBinder',  # overwrite abc

    'DynamicDictItem',
    'DynamicListItem',

    'DynamicText',

    'view'
]


def update_events(method):
    """Use this decorator to make a method update the events transmissions."""

    def wrapper(self: abc.DynamicContainer, *args, **kwargs):
        self._clear_events()
        result = method(self, *args, **kwargs)
        self._setup_events()
        return result

    return wrapper


def view(value: Any) -> Any:
    if isinstance(value, abc.Dynamic):
        return value.view()

    else:
        return value


def dynamic(data: object) -> object:
    if isinstance(data, abc.Dynamic):
        return data

    elif isinstance(data, dict):
        return DynamicDict(data)

    elif isinstance(data, list):
        return DynamicList(data)

    else:
        return data


class DynamicDict(dict, abc.DynamicContainer):
    def __init__(self, data: dict = None):
        if data is None:
            data = {}

        dict.__init__(self)

        for key, val in data.items():
            self[key] = val

    def __repr__(self):
        return f"{self.__class__.__name__}({dict.__repr__(self)})"

    def _setup_events(self):
        for key, value in self.items():
            if isinstance(value, Emitter):
                self.transmit(name='*', emitter=value, prefix=f".{key}")

    def _clear_events(self):
        for value in self.values():
            if isinstance(value, Emitter):
                self.forget(name='*', emitter=value)

    def __getitem__(self, key: str):
        return dict.__getitem__(self, key)

    @update_events
    def __setitem__(self, key: str, value):
        try:
            socket = dict.__getitem__(self, key)

        except KeyError:
            socket = None

        if isinstance(socket, abc.DynamicBinder):
            socket.set(value)
            self.emit(f".{key}", key=key, value=socket.view())

        elif isinstance(socket, abc.DynamicContainer):
            socket.update_with(value)

        else:
            value = dynamic(value)
            dict.__setitem__(self, key, value)
            self.emit(f".{key}", key=key, value=value)

    @update_events
    def __delitem__(self, key: str) -> None:
        dict.__delitem__(self, key)
        self.emit(f".{key}:del", key=key)

    @update_events
    def pop(self, key: str) -> None:
        value = dict.pop(self, key)
        self.emit(f".{key}:pop", key=key)
        return value

    def update_with(self, data):
        if isinstance(data, DynamicDict):
            raise ValueError

        elif isinstance(data, dict):
            for key, val in data.items():
                self[key] = val

        else:
            raise TypeError

    def view(self) -> dict:
        return {
            key: value.view() if isinstance(value, abc.Dynamic) else value
            for key, value in self.items()
        }


class DynamicList(list, abc.DynamicContainer):
    def __init__(self, data: list = None):
        if data is None:
            data = {}

        list.__init__(self)

        for element in data:
            self.append(element)

    def __repr__(self):
        return f"{self.__class__.__name__}({list.__repr__(self)})"

    def _setup_events(self):
        for index, element in enumerate(self):
            if isinstance(element, Emitter):
                self.transmit(name='*', emitter=element, prefix=f".{index}")

    def _clear_events(self):
        for element in self:
            if isinstance(element, Emitter):
                self.forget(name='*', emitter=element)

    def __getitem__(self, index: int):
        return list.__getitem__(self, index)

    @update_events
    def __setitem__(self, index: int, element):
        try:
            socket = list.__getitem__(self, index)

        except IndexError:
            socket = None

        if isinstance(socket, abc.DynamicBinder):
            socket.set(element)

        elif isinstance(socket, abc.DynamicContainer):
            socket.update_with(element)

        else:
            element = dynamic(element)
            list.__setitem__(self, index, element)
            self.emit(f".{index}", index=index, element=element)

    @update_events
    def append(self, element):
        element = dynamic(element)
        list.append(self, element)
        self.emit(f":append", index=len(self) - 1, element=element)

    @update_events
    def insert(self, index: int, element):
        element = dynamic(element)
        list.insert(self, index, element)
        self.emit(f":insert", index=index, element=element)

    @update_events
    def remove(self, element):
        index = self.index(element)
        list.remove(self, element)
        self.emit(f":remove", index=index, element=element)

    @update_events
    def pop(self, index: int = -1):
        element = list.pop(self, index)
        self.emit(f":pop", index=index, element=element)
        return element

    def view(self) -> list:
        return [
            element.view() if isinstance(element, abc.Dynamic) else element
            for element in self
        ]

    def update_with(self, data):
        if isinstance(data, DynamicList):
            raise TypeError

        elif isinstance(data, list):
            while self:
                self.pop(-1)  # type: ignore

            for element in data:
                self.append(element)

        else:
            raise TypeError


class DynamicBinder(abc.DynamicBinder, ABC):
    def view(self):
        return view(self.get())

    @classmethod
    def from_evaluable(cls, evaluable, data):
        if isinstance(evaluable, EvaluableListItem):
            return DynamicListItem(data=data, index=evaluable.index)

        elif isinstance(evaluable, EvaluableDictItem):
            return DynamicDictItem(data=data, key=evaluable.key)

        elif isinstance(evaluable, EvaluablePath):
            for step in evaluable.steps:
                data = cls.from_evaluable(step, data)

            return data

        else:
            raise TypeError(type(evaluable))

    def __len__(self):
        return self.get().__len__()

    def __getitem__(self, item):
        return self.get().__getitem__(item)

    def __setitem__(self, item, value):
        self.get().__setitem__(item, value)


@dataclass
class DynamicDictItem(DynamicBinder):
    data: dict
    key: str

    def __post_init__(self):
        if isinstance(self.data, Emitter):
            self.transmit_without_prefix(emitter=self.data, prefix=f".{self.key}")

    def get(self) -> object:
        return self.data[self.key]

    def set(self, value: object):
        self.data[self.key] = value

    def update(self, key: str) -> None:
        self.key = key
        self.emit(name='', key=key)


@dataclass
class DynamicListItem(DynamicBinder):
    data: list
    index: int

    def __post_init__(self):
        if isinstance(self.data, Emitter):
            self.transmit_without_prefix(emitter=self.data, prefix=f".{self.index}")

    def get(self) -> object:
        return self.data[self.index]

    def set(self, value: object) -> None:
        self.data[self.index] = value

    def update(self, index: int) -> None:
        self.index = index
        self.emit(name='', index=index)


@dataclass
class DynamicText(abc.Dynamic):
    expression: str
    values: List[abc.DynamicBinder]

    def view(self) -> str:
        return self.expression.format(*map(str, map(view, self.values)))
