from . import base, factory

(
    Event,
    EventModel,
    Emitter,
    Observer,
    Transmitter
) = factory.new_event_system(event_manager_factory=base.QueueEventManager)
