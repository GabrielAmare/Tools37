import re
from abc import ABC
from collections import deque
from dataclasses import dataclass, field, replace
from typing import Optional, Dict, List, ClassVar, Tuple, Deque, Type, Union

from . import abc

__all__ = [
    'BaseEventManager',
    'DirectEventManager',
    'QueueEventManager',
    'Event',
    'EventModel',
    'Emitter',
    'Observer',
    'Transmitter'
]

from tools37.console import LogConsole

console = LogConsole(width=200)
DEBUG = False


@dataclass
class BaseEventManager(abc.EventManager, ABC):
    functions: Dict[abc.EventModel, List[abc.EVENT_FUNCTION]] = field(default_factory=dict)

    def register_function(self, model, function):
        self.functions.setdefault(model, [])
        functions = self.functions[model]
        if function not in functions:
            functions.append(function)

    def unregister_function(self, model, function):
        if model in self.functions:
            if function in self.functions[model]:
                self.functions[model].remove(function)

    def unregister_model(self, model):
        if model in self.functions:
            del self.functions[model]


@dataclass
class DirectEventManager(BaseEventManager):
    """This kind of event managers apply events as soon as they are registered."""

    def register_event(self, event):
        if DEBUG:
            console.success("\n".join(f"{key!s} -> {value!r}" for key, value in event.__dict__.items()))

        for model, callbacks in self.functions.copy().items():
            if model.match(event):
                for callback in callbacks:
                    callback(event)


@dataclass
class QueueEventManager(BaseEventManager):
    """This kind of event managers apply events only when the .update method is called."""

    queue: Deque[abc.Event] = field(default_factory=deque)

    def register_event(self, event):
        self.queue.append(event)

    def update(self):
        """This method will apply all the events in queue then remove them."""
        while self.queue:
            event = self.queue.popleft()
            for model, callbacks in self.functions.copy().items():
                if model.match(event):
                    for callback in callbacks:
                        callback(event)


def remove_prefix(string: str, prefix: str) -> str:
    if prefix:
        return string[len(prefix):]

    else:
        return string


def remove_suffix(string: str, suffix: str) -> str:
    if suffix:
        return string[:-len(suffix)]

    else:
        return string


@dataclass
class Event(abc.Event):
    _manager: ClassVar[abc.EventManager]

    emitter: Optional[object] = None
    name: str = ''
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)

    def emit(self):
        self._manager.register_event(self)

    def remove_prefix(self, prefix: str) -> abc.Event:
        return replace(self, name=remove_prefix(self.name, prefix))

    def remove_suffix(self, suffix: str) -> abc.Event:
        return replace(self, name=remove_suffix(self.name, suffix))

    def append_prefix(self, prefix: str) -> abc.Event:
        return replace(self, name=prefix + self.name)

    def append_suffix(self, suffix: str) -> abc.Event:
        return replace(self, name=self.name + suffix)

    def with_emitter(self, emitter):
        return replace(self, emitter=emitter)


class EventModel(abc.EventModel):
    _manager: ClassVar[abc.EventManager]

    __instances: ClassVar[Dict[Tuple[int, int, int], abc.EventModel]] = {}

    __slots__ = ('name', 'observer', 'emitter')

    name: Union[str, re.Pattern]
    observer: Optional[object]
    emitter: Optional[object]

    def __new__(cls, name: Union[str, re.Pattern], observer=None, emitter=None):
        key = (id(observer), id(emitter), hash(name))

        try:
            instance = cls.__instances[key]

        except KeyError:
            cls.__instances[key] = instance = super().__new__(cls)
            instance.name = name
            instance.observer = observer
            instance.emitter = emitter

        return instance

    def __hash__(self):
        return hash((id(self.observer), id(self.emitter), hash(self.name)))

    def triggers(self, function):
        self._manager.register_function(self, function)

    def forget(self, function=None):
        if function is None:
            self._manager.unregister_model(self)
        else:
            self._manager.unregister_function(self, function)

    def match(self, event: Event) -> bool:
        if self.emitter is not event.emitter:
            return False

        if isinstance(self.name, str):
            if self.name == '*':
                return True

            elif self.name == event.name:
                return True

            else:
                return False

        elif isinstance(self.name, re.Pattern):
            raise NotImplementedError

        else:
            return False


class Emitter(abc.Emitter):
    _event_factory: ClassVar[Type[abc.Event]]

    def _create_event(self, name, args, kwargs):
        return self._event_factory(emitter=self, name=name, args=args, kwargs=kwargs)

    def emit(self, name: str, *args, **kwargs):
        event = self._create_event(name=name, args=args, kwargs=kwargs)
        event.emit()


class Observer(abc.Observer):
    _event_model_factory: ClassVar[Type[abc.EventModel]]

    def _create_event_model(self, name, emitter):
        return self._event_model_factory(name=name, observer=self, emitter=emitter)

    def on(self, name, emitter, function):
        model = self._create_event_model(name, emitter)
        model.triggers(function)

    def forget(self, emitter, name):
        model = self._create_event_model(name, emitter)
        model.forget()


class Transmitter(Observer, Emitter, abc.Transmitter):
    def transmit(self, name, emitter, prefix=''):
        model = self._create_event_model(name, emitter)

        def function(event: Event) -> None:
            event.append_prefix(prefix).with_emitter(self).emit()

        model.triggers(function)

    def transmit_without_prefix(self, emitter, prefix=''):
        model = self._create_event_model(name='*', emitter=emitter)

        def function(event: Event):
            if event.name.startswith(prefix):
                event.remove_prefix(prefix).with_emitter(self).emit()

        model.triggers(function)
