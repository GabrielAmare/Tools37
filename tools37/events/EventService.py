from typing import Dict, List, Callable


class EventService:
    _callbacks: Dict[int, Dict[str, List[callable]]] = {}

    @classmethod
    def on(cls, obj: object, evt: str, callback: callable) -> Callable[[], None]:
        uid = id(obj)
        cls._callbacks.setdefault(uid, {})
        cls._callbacks[uid].setdefault(evt, [])
        cls._callbacks[uid][evt].append(callback)

        def unsubscribe():
            if uid in cls._callbacks:
                if evt in cls._callbacks[uid]:
                    if callback in cls._callbacks[uid][evt]:
                        cls._callbacks[uid][evt].remove(callback)

        return unsubscribe

    @classmethod
    def emit(cls, obj: object, evt: str, *args, **kwargs) -> None:
        uid = id(obj)
        for callback in cls._callbacks.get(uid, {}).get(evt, []):
            callback(*args, **kwargs)


def emittermethod(key) -> Callable[[callable], callable]:
    """Whenever the wrapped method is called, it will emit the `key` event."""

    def wrapper(method: callable) -> callable:
        def wrapped(self: object, *args, **kwargs):
            EventService.emit(self, key, *args, **kwargs)
            return method(self, *args, **kwargs)

        return wrapped

    return wrapper
