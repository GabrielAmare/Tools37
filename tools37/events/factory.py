from . import abc, base
from typing import Type, Tuple


def new_event_system(event_manager_factory: Type[abc.EventManager]) -> Tuple[Type[abc.Event], Type[abc.EventModel], Type[abc.Emitter], Type[abc.Observer], Type[abc.Transmitter]]:
    event_manager = event_manager_factory()

    class Event(base.Event):
        _manager = event_manager

    class EventModel(base.EventModel):
        _manager = event_manager

    class Emitter(base.Emitter):
        _event_factory = Event

    class Observer(base.Observer):
        _event_model_factory = EventModel

    class Transmitter(Emitter, Observer, base.Transmitter):
        _event_factory = Event
        _event_model_factory = EventModel

    return Event, EventModel, Emitter, Observer, Transmitter
