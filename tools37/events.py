from typing import Dict, Callable, Union
from typing import List


class EventService:
    _callbacks: Dict[str, List[callable]] = {}

    @classmethod
    def on(cls, evt: str, callback: callable) -> Callable[[], None]:
        cls._callbacks.setdefault(evt, [])
        cls._callbacks[evt].append(callback)

        def forget():
            if evt in cls._callbacks:
                if callback in cls._callbacks[evt]:
                    cls._callbacks[evt].remove(callback)

        return forget

    @classmethod
    def emit(cls, evt: str, *args, **kwargs) -> None:
        for callback in cls._callbacks.get(evt, []):
            callback(*args, **kwargs)


def _object_event(obj: object, evt: str) -> str:
    return f"{id(obj)}/{evt}"


class emitmethod:
    @staticmethod
    def _before(method: callable, evt: str):
        def wrapped(self: object, *args, **kwargs):
            EventService.emit(_object_event(self, evt), *args, **kwargs)
            return method(self, *args, **kwargs)

        return wrapped

    @staticmethod
    def _after(method: callable, evt: str):
        def wrapped(self: object, *args, **kwargs):
            result = method(self, *args, **kwargs)
            EventService.emit(_object_event(self, evt), *args, **kwargs)
            return result

        return wrapped

    @classmethod
    def _apply(cls, __evt, __wrapper) -> Union[callable, Callable[[callable], callable]]:
        if isinstance(__evt, str):
            return lambda method: __wrapper(method, __evt)
        elif hasattr(__evt, '__call__'):
            return cls._before(__evt, __evt.__name__)
        else:
            raise ValueError(__evt)

    @classmethod
    def before(cls, __evt):
        return cls._apply(__evt, cls._before)

    @classmethod
    def after(cls, __evt):
        return cls._apply(__evt, cls._after)


class Emitter:
    """Add an `emit` method which emits an event as `self`."""

    def emit(self, evt: str, *args, **kwargs):
        """Emit ``key`` with some args & kwargs"""
        EventService.emit(_object_event(self, evt), *args, **kwargs)


class Observer:
    """Add an `on` method which subscribe to an event of `obj`"""

    def on(self, obj: Emitter, evt: str, callback: callable):
        """Register a ``callback`` for further emits of ``key``"""
        EventService.on(_object_event(obj, evt), callback)


class Transmitter(Emitter, Observer):
    """Add a `transmit` method which re-emit the `evt` emitted by `obj` as `self`"""

    def transmit(self, obj: Emitter, evt: str):
        def callback(*args, **kwargs):
            self.emit(evt, *args, **kwargs)

        self.on(obj, evt, callback)


class EmitterList(Emitter, list):
    """This list subclass emit events whenever its items are modified."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"

    __setitem__ = emitmethod.after(list.__setitem__)
    append = emitmethod.after(list.append)
    remove = emitmethod.after(list.remove)
    insert = emitmethod.after(list.insert)
    pop = emitmethod.after(list.pop)
