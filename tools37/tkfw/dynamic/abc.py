from abc import ABC, abstractmethod
from typing import Any

from tools37.tkfw._commented.events import Transmitter

__all__ = [
    'Dynamic',
    'DynamicContainer',
    'DynamicBinder',
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
    @abstractmethod
    def _setup_events(self) -> None:
        """Build all the required events transmissions."""

    @abstractmethod
    def _clear_events(self) -> None:
        """Remove all the events transmissions."""

    @abstractmethod
    def update_with(self, data: Any) -> None:
        """"""


class DynamicBinder(Dynamic, ABC):
    @abstractmethod
    def get(self) -> Any:
        """"""

    @abstractmethod
    def set(self, value: Any) -> None:
        """"""
