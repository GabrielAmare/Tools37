from abc import ABC
from dataclasses import dataclass
from typing import List, Optional, Any

from . import abc
from ..evaluable import EvaluableGetter, EvaluableSetter, EvaluableBinder, as_evaluable_text
from ..events import Emitter

__all__ = [
    'DynamicDict',  # overwrite abc
    'DynamicList',  # overwrite abc

    'DynamicDictItem',
    'DynamicListItem',

    'DynamicText',

    'DynamicData',  # overwrite abc
    'DynamicStyle',  # overwrite abc

    'DynamicGetter',
    'DynamicSetter',
    'DynamicBinder',

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


class DynamicDict(dict, abc.DynamicDict):
    def __init__(self, data: dict = None):
        self._is_init = True

        if data is None:
            data = {}

        dict.__init__(self)

        for key, val in data.items():
            self[key] = val

        self._is_init = True

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    def _setup_events(self):
        if self._is_init:
            for key, value in self.items():
                if isinstance(value, Emitter):
                    self.transmit(name='*', emitter=value, prefix=f".{key}")

    def _clear_events(self):
        if self._is_init:
            for value in self.values():
                if isinstance(value, Emitter):
                    self.forget(name='*', emitter=value)

    def __getitem__(self, key: str):
        return dict.__getitem__(self, key)

    @update_events
    def __setitem__(self, key, value):
        try:
            socket = dict.__getitem__(self, key)

            if isinstance(socket, abc.DynamicSetter):
                socket.set(value)
                self.emit(f".{key}", key=key, value=socket.view())

            elif isinstance(socket, abc.DynamicContainer):
                socket.update_with(value)

            else:
                value = self.__class__._value_parser(value)
                dict.__setitem__(self, key, value)
                if self._is_init:
                    self.emit(f".{key}", key=key, value=value)

        except (KeyError, ValueError, AttributeError, TypeError):
            value = self.__class__._value_parser(value)
            dict.__setitem__(self, key, value)
            if self._is_init:
                self.emit(f".{key}", key=key, value=value)

    @update_events
    def __delitem__(self, key):
        dict.__delitem__(self, key)

    @update_events
    def pop(self, key):
        value = super().pop(key)
        self.emit(f".{key}:pop", key=key, value=value)
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


class DynamicList(list, abc.DynamicList):
    def __init__(self, data: list = None):
        self._is_init = True
        if data is None:
            data = {}

        list.__init__(self)

        for element in data:
            self.append(element)

        self._is_init = True

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    def _setup_events(self):
        if self._is_init:
            for index, element in enumerate(self):
                if isinstance(element, Emitter):
                    self.transmit(name='*', emitter=element, prefix=f".{index}")

    def _clear_events(self):
        if self._is_init:
            for element in self:
                if isinstance(element, Emitter):
                    self.forget(name='*', emitter=element)

    def __getitem__(self, index: int):
        return list.__getitem__(self, index)

    @update_events
    def __setitem__(self, index: int, element):
        try:
            socket = self[index]
            if isinstance(socket, abc.DynamicSetter):
                socket.set(element)

            elif isinstance(socket, abc.DynamicContainer):
                socket.update_with(element)

            else:
                element = self.__class__._value_parser(element)
                list.__setitem__(self, index, element)
                self.emit(f".{index}", index=index, element=element)

        except (IndexError, ValueError, AttributeError, TypeError):
            element = self.__class__._value_parser(element)
            list.__setitem__(self, index, element)
            self.emit(f".{index}", index=index, element=element)

    @update_events
    def append(self, element):
        element = self.__class__._value_parser(element)
        list.append(self, element)
        if self._is_init:
            self.emit(f":append", index=len(self) - 1, element=element)

    @update_events
    def insert(self, index: int, element):
        element = self.__class__._value_parser(element)
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


def value_parser(value: object) -> object:
    if isinstance(value, abc.Dynamic):
        return value

    elif isinstance(value, dict):
        return DynamicDict(value)

    elif isinstance(value, list):
        return DynamicList(value)

    else:
        return value


DynamicDict._value_parser = value_parser
DynamicList._value_parser = value_parser


class DynamicGetter(abc.DynamicGetter, ABC):
    def view(self):
        return view(self.get())


@dataclass
class DynamicDictItem(DynamicGetter, abc.DynamicBinder):
    data: dict
    key: str

    def __post_init__(self):
        if isinstance(self.data, Emitter):
            self.transmit_without_prefix(emitter=self.data, prefix=f".{self.key}")

    def get(self) -> object:
        return self.data[self.key]

    def set(self, value: object):
        self.data[self.key] = value


@dataclass
class DynamicListItem(DynamicGetter, abc.DynamicBinder):
    data: list
    index: int

    def __post_init__(self):
        if isinstance(self.data, Emitter):
            self.transmit_without_prefix(emitter=self.data, prefix=f".{self.index}")

    def get(self) -> object:
        return self.data[self.index]

    def set(self, value: object) -> None:
        self.data[self.index] = value


@dataclass
class DynamicText(abc.Dynamic):
    expression: str
    values: List[abc.DynamicGetter]

    def view(self) -> str:
        return self.expression.format(*map(str, map(view, self.values)))


class DynamicData(DynamicDict, abc.DynamicData):
    """
        DynamicDict with optional inheritance.
        - allow to set parent item, if local data doesn't already contains the key.
    """

    def __init__(self, data: dict = None, parent_data: abc.DynamicData = None):
        self.parent_data: Optional[abc.DynamicData] = parent_data
        DynamicDict.__init__(self, data)

    def __setitem__(self, key, value):
        if self.parent_data and key in self.parent_data and not DynamicDict.__contains__(self, key):
            self.parent_data[key] = value

        else:
            DynamicDict.__setitem__(self, key, value)

    def __getitem__(self, key):
        if DynamicDict.__contains__(self, key):
            return DynamicDict.__getitem__(self, key)

        elif self.parent_data:
            return self.parent_data[key]

        else:
            raise KeyError(key)

    def view(self) -> dict:
        data = {}

        if self.parent_data:
            data.update(self.parent_data.view())

        data.update(super().view())

        return data


class DynamicStyle(DynamicDict, abc.DynamicStyle):
    """
        DynamicDict with optional inheritance.
        - doesn't allow to set parent properties.
        - parse str values to DynamicTextModel if possible.
    """

    def __init__(self, style: dict = None, parent_style: abc.DynamicStyle = None):
        self.parent_style: Optional[abc.DynamicStyle] = parent_style
        DynamicDict.__init__(self, style)

    def __setitem__(self, key, value):
        if isinstance(value, str):
            value = as_evaluable_text(string=value)

        DynamicDict.__setitem__(self, key, value)

    def __getitem__(self, key):
        if DynamicDict.__contains__(self, key):
            return DynamicDict.__getitem__(self, key)

        elif self.parent_style:
            return self.parent_style[key]

        else:
            raise KeyError(key)

    def view(self) -> dict:
        style = {}

        if self.parent_style:
            style.update(self.parent_style.view())

        style.update(DynamicDict.view(self))

        return style


@dataclass
class DynamicSetter(abc.DynamicSetter):
    data: Any
    path: EvaluableSetter

    def set(self, value: Any) -> Any:
        self.path.set(self.data, value)

    def view(self) -> Any:
        raise Exception(f"{self.evaluable!s} is set only !")


@dataclass
class DynamicGetter(abc.DynamicGetter):
    data: Any
    path: EvaluableGetter

    def __post_init__(self):
        self.transmit_without_prefix(emitter=self.data, prefix=f".{self.path!s}")

    def get(self) -> Any:
        return self.path.get(self.data)

    def view(self) -> Any:
        return view(self.path.evaluate(self.data))


@dataclass
class DynamicBinder(abc.DynamicBinder):
    data: Any
    path: EvaluableBinder

    def __post_init__(self):
        self.transmit_without_prefix(emitter=self.data, prefix=f".{self.path!s}")

    def get(self) -> Any:
        self.path.get(self.data)

    def set(self, value: Any) -> Any:
        self.path.set(self.data, value)

    def view(self) -> Any:
        return view(self.path.evaluate(self.data))
