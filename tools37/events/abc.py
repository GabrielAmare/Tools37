from abc import ABC, abstractmethod
from typing import Callable, ClassVar, Type, Optional

__all__ = [
    'Event',
    'EVENT_FUNCTION',
    'EventModel',
    'EventManager',
    'Emitter',
    'Observer',
    'Transmitter'
]


class Event(ABC):
    @abstractmethod
    def emit(self) -> None:
        """Emit the event to it's manager."""

    @abstractmethod
    def with_emitter(self, emitter) -> 'Event':
        """Return a copy of the event with a new emitter."""


EVENT_FUNCTION = Callable[[Event], None]


class EventModel(ABC):
    @abstractmethod
    def __hash__(self):
        """return hash(self)"""

    @abstractmethod
    def triggers(self, callback: EVENT_FUNCTION):
        """Whenever an event is matched by `self`, it will call the function with `event` as an argument."""

    @abstractmethod
    def match(self, event: Event) -> bool:
        """Return True if the given `event` is match the model."""

    @abstractmethod
    def forget(self) -> None:
        """The functions (registered using self.triggers) will no longer be called when events are matching `self`."""


class EventManager(ABC):
    @abstractmethod
    def register_event(self, event: Event) -> None:
        """Register an `event`."""

    @abstractmethod
    def register_function(self, model: EventModel, function: EVENT_FUNCTION) -> None:
        """Register a `function` in the `model` functions."""

    @abstractmethod
    def unregister_model(self, model: EventModel) -> None:
        """Remove all the registered `model` functions."""

    @abstractmethod
    def unregister_function(self, model: EventModel, function: EVENT_FUNCTION) -> None:
        """Remove a specific registered `function` of `model` functions."""


class Emitter(ABC):
    _event_factory: ClassVar[Type[Event]]

    @abstractmethod
    def _create_event(self, name, args, kwargs):
        """"""

    @abstractmethod
    def emit(self, name: str, *args, **kwargs):
        """"""


class Observer(ABC):
    _event_model_factory: ClassVar[Type[EventModel]]

    @abstractmethod
    def _create_event_model(self, name: str, emitter: Optional[Emitter]) -> EventModel:
        """"""

    @abstractmethod
    def on(self, name: str, emitter: Optional[Emitter], function: EVENT_FUNCTION) -> None:
        """"""

    @abstractmethod
    def forget(self, emitter: Optional[Emitter], name: str) -> None:
        """"""


class Transmitter(Observer, Emitter, ABC):
    @abstractmethod
    def transmit(self, name: str, emitter: Optional[Emitter], prefix: str = '') -> None:
        """"""

    @abstractmethod
    def transmit_without_prefix(self, emitter: Optional[Emitter], prefix: str = '') -> None:
        """"""
