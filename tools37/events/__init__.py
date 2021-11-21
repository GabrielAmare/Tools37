from .factory import new_event_system
from .base import DirectEventManager

Event, EventModel, Emitter, Observer, Transmitter = new_event_system(event_manager_factory=DirectEventManager)
