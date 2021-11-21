from abc import ABC, abstractmethod
from typing import Any, Callable, ClassVar

from ..events import Transmitter

__all__ = [
    'Dynamic',
    'DynamicContainer',

    'DynamicDict',
    'DynamicList',

    'DynamicGetter',
    'DynamicSetter',
    'DynamicBinder',

    'DynamicData',
    'DynamicStyle'
]


class Dynamic(Transmitter, ABC):
    """
        HasView objects are dynamic objects.
        They must implement a view method which return the current state of the data.
    """

    @abstractmethod
    def view(self) -> Any:  # non HasView
        """Return a static view of the object. The must never contains any reference to HasView instances."""


class DynamicContainer(Dynamic, ABC):
    _value_parser: ClassVar[Callable[[object], object]]

    @abstractmethod
    def _setup_events(self) -> None:
        """Build all the required events transmissions."""

    @abstractmethod
    def _clear_events(self) -> None:
        """Remove all the events transmissions."""

    @abstractmethod
    def update_with(self, data: Any) -> None:
        """"""


class DynamicDict(DynamicContainer, ABC):
    @abstractmethod
    def __init__(self, data: dict = None):
        """"""

    @abstractmethod
    def __getitem__(self, key: str) -> object:
        """"""

    @abstractmethod
    def __setitem__(self, key: str, value: object):
        """"""

    @abstractmethod
    def __delitem__(self, key: str) -> None:
        """"""

    @abstractmethod
    def pop(self, key: str) -> object:
        """"""

    @abstractmethod
    def view(self) -> dict:
        """"""

    @abstractmethod
    def update_with(self, data: dict) -> None:
        """"""


class DynamicList(DynamicContainer, ABC):
    @abstractmethod
    def __init__(self, data: list = None):
        """"""

    @abstractmethod
    def __getitem__(self, index: int) -> object:
        """"""

    @abstractmethod
    def __setitem__(self, index: int, element: object) -> None:
        """"""

    @abstractmethod
    def __delitem__(self, index: int) -> None:
        """"""

    @abstractmethod
    def append(self, element: object) -> None:
        """"""

    @abstractmethod
    def insert(self, index: int, element: object) -> None:
        """"""

    @abstractmethod
    def remove(self, element: object) -> None:
        """"""

    @abstractmethod
    def pop(self, index: int = -1) -> object:
        """"""

    @abstractmethod
    def view(self) -> list:
        """"""

    @abstractmethod
    def update_with(self, data: list) -> None:
        """"""


class DynamicGetter(Dynamic, ABC):
    @abstractmethod
    def get(self) -> Any:
        """"""


class DynamicSetter(Dynamic, ABC):
    @abstractmethod
    def set(self, value: Any) -> None:
        """"""


class DynamicBinder(DynamicGetter, DynamicSetter, ABC):
    """"""


class DynamicData(DynamicDict, ABC):
    @abstractmethod
    def __init__(self, data: dict = None, parent_data: DynamicDict = None):
        """"""


class DynamicStyle(DynamicDict, ABC):
    @abstractmethod
    def __init__(self, style: dict = None, parent_style: DynamicDict = None):
        """"""
