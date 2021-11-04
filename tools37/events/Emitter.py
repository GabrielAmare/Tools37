from .EventService import EventService


class Emitter:
    def emit(self, key: str, *args, **kwargs):
        """Emit ``key`` with some args & kwargs"""
        EventService.emit(self, key, *args, **kwargs)

    def on(self, key: str, callback: callable):
        """Register a ``callback`` for further emits of ``key``"""
        EventService.on(self, key, callback)

    @staticmethod
    def method_decorator(key):
        """Binds a method call to emit ``key`` with the method arguments"""

        def wrapper(method):
            """Wraps around a method of an Emitter subclass"""

            def wrapped(self: Emitter, *args, **kwargs):
                self.emit(key, *args, **kwargs)
                return method(self, *args, **kwargs)

            return wrapped

        return wrapper
