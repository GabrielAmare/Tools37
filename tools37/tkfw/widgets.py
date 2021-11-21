import tkinter as tk

from .tree_roles import Root, Node, Leaf


class Tk(tk.Tk, Root):
    def __init_subclass__(cls, **kwargs):
        cls._init_tree_class(kwargs)

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
        cls._init_tree_class(kwargs)

    def __init__(self, parent, data: dict = None, style: dict = None):
        tk.Frame.__init__(self, parent)
        Node.__init__(self, parent, data, style)


class LabelFrame(tk.LabelFrame, Node):
    def __init_subclass__(cls, **kwargs):
        cls._init_tree_class(kwargs)

    def __init__(self, parent, data: dict = None, style: dict = None):
        tk.LabelFrame.__init__(self, parent)
        Node.__init__(self, parent, data, style)


class Label(tk.Label, Leaf):
    def __init_subclass__(cls, **kwargs):
        cls._init_tree_class(kwargs)

    def __init__(self, parent, data: dict = None, style: dict = None):
        tk.Label.__init__(self, parent)
        Leaf.__init__(self, parent, data, style)


class Button(tk.Button, Leaf):
    def __init_subclass__(cls, **kwargs):
        cls._init_tree_class(kwargs)

    def __init__(self, parent, data: dict = None, style: dict = None):
        tk.Button.__init__(self, parent)
        Leaf.__init__(self, parent, data, style)

        if hasattr(self, 'command') and hasattr(self.command, '__call__'):
            self.config(command=self.command)


class Entry(tk.Entry, Leaf):
    def __init_subclass__(cls, **kwargs):
        cls._init_tree_class(kwargs)

    def __init__(self, parent, data: dict = None, style: dict = None):
        tk.Entry.__init__(self, parent)
        Leaf.__init__(self, parent, data, style)

        self._variable = tk.StringVar(self, value=self._value_getter.view() if self._value_getter else '')
        self.config(textvariable=self._variable)

        if self._value_setter:
            self.bind('<Any-KeyRelease>', self._update_model)

    def _get_local(self):
        return self._variable.get()

    def _set_local(self, value):
        self._variable.set(value)
