from .Component import Component

__all__ = [
    'Root',
    'Node',
    'Leaf'
]


class Leaf(Component):
    def update_widgets(self):
        pass

    def __getattr__(self, key):
        try:
            return super().__getattribute__(key)

        except AttributeError:
            if self.parent:
                return getattr(self.parent, key)

            else:
                raise AttributeError(key)


class Node(Component):
    def _set_local(self, value):
        raise Exception

    def _get_local(self):
        raise Exception

    def __getattr__(self, key):
        try:
            return super().__getattribute__(key)

        except AttributeError:
            if self.parent:
                return getattr(self.parent, key)

            else:
                raise AttributeError(key)


class Root(Component):
    def _set_local(self, value):
        raise Exception

    def _get_local(self):
        raise Exception
