import tkinter as tk

from .roles import Root, Node, Leaf
from .utils import Horizontal, Vertical, Fill
from ..dynamic import DynamicBinder

__all__ = [
    'Tk',
    'Frame',
    'LabelFrame',
    'Label',
    'Button',
    'Entry',
    'Row', 'Column', 'LargeRow', 'LargeColumn'
]


class Tk(tk.Tk, Root):
    def __init_subclass__(cls, **kwargs):
        cls._init_component_class(kwargs)

    def __init__(self, data: dict = None):
        tk.Tk.__init__(self)
        Root.__init__(self, None, data)

        self.update()

    def _update(self, fps: int) -> None:
        self.update()
        self.after(int(1000 // fps), self._update, fps)

    def run(self, fps: int = 60):
        self._update(fps)
        self.mainloop()


class Frame(tk.Frame, Node):
    def __init_subclass__(cls, **kwargs):
        cls._init_component_class(kwargs)

    def __init__(self, parent, data: dict = None, style: dict = None):
        tk.Frame.__init__(self, parent)
        Node.__init__(self, parent, data, style)


class LabelFrame(tk.LabelFrame, Node):
    def __init_subclass__(cls, **kwargs):
        cls._init_component_class(kwargs)

    def __init__(self, parent, data: dict = None, style: dict = None):
        tk.LabelFrame.__init__(self, parent)
        Node.__init__(self, parent, data, style)


class Label(tk.Label, Leaf):
    def __init_subclass__(cls, **kwargs):
        cls._init_component_class(kwargs)

    def __init__(self, parent, data: dict = None, style: dict = None):
        tk.Label.__init__(self, parent)
        Leaf.__init__(self, parent, data, style)


class Button(tk.Button, Leaf):
    def __init_subclass__(cls, **kwargs):
        cls._init_component_class(kwargs)

    def __init__(self, parent, data: dict = None, style: dict = None):
        tk.Button.__init__(self, parent)
        Leaf.__init__(self, parent, data, style)

        if hasattr(self, 'command') and hasattr(self.command, '__call__'):
            self.config(command=self.command)


class Entry(tk.Entry, Leaf):
    def __init_subclass__(cls, **kwargs):
        cls._init_component_class(kwargs)

    def __init__(self, parent, data: dict = None, style: dict = None):
        tk.Entry.__init__(self, parent)
        Leaf.__init__(self, parent, data, style)

        self._variable = tk.StringVar(self, value=self.binder.view() if isinstance(self.binder, DynamicBinder) else '')
        self.config(textvariable=self._variable)

        if isinstance(self.binder, DynamicBinder):
            self.bind('<Any-KeyRelease>', self._update_model)

    def _get_local(self):
        return self._variable.get()

    def _set_local(self, value):
        self._variable.set(value)


class Row(Frame, Horizontal):
    pass


class Column(Frame, Vertical):
    pass


class LargeRow(Frame, Horizontal, Fill):
    pass


class LargeColumn(Frame, Vertical, Fill):
    pass
