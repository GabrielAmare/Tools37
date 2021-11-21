import tkinter as tk
from abc import ABC, ABCMeta
from typing import Optional, ClassVar, Callable, List, Type

from . import abc
from ..behaviours import HasLogic, HasIter, HasValue, HasStyleAndData
from ..core_utils import Horizontal, Vertical, Centered
from ..dynamic import Dynamic, DynamicData, DynamicStyle, DynamicList, DynamicListItem
from ..evaluable import Evaluable
from ..events import Observer, Event, Emitter
from ..grid_methods import grid_centered_vertically, grid_vertically, grid_centered_horizontally, grid_horizontally

__all__ = [
    'WidgetBuilder',
    'ListWidgetBuilder',
    'UnitWidgetBuilder',

    'GridManager',

    'Parent',
    'Child',
    'Tree'
]


def _check_style_render_integrity(style: dict):
    assert isinstance(style, dict)
    for key, value in style.items():
        assert isinstance(key, str)
        if isinstance(value, (Evaluable, Dynamic)):
            raise Exception(f"Style error : {key!s}={value!r} should not be Evaluable | Dynamic")


def _get_class_attr(cls, key, kwargs, default):
    if key in kwargs:
        return kwargs[key]

    elif key in cls.__dict__:
        return cls.__dict__[key]

    else:
        return default


class WidgetBuilder(Observer, abc.WidgetBuilder, ABC):
    parent: abc.Parent
    factory: Type[abc.Child]

    def __init__(self, parent: abc.Parent, factory: Type[abc.Child]):
        self.parent: abc.Parent = parent
        self.factory: Type[abc.Child] = factory

    def create(self, data: dict = None, style: dict = None) -> abc.Child:
        return self.factory(parent=self.parent, data=data, style=style)

    def should_build(self) -> bool:
        return self.factory.evaluate_condition(data=self.parent.data)


class UnitWidgetBuilder(WidgetBuilder, abc.UnitWidgetBuilder):
    """"""
    widget: Optional[abc.Child]

    def __init__(self, parent: abc.Parent, factory: Type[abc.Child]):
        super().__init__(parent, factory)
        self.widget: Optional[abc.Child] = None

        self.build()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.parent!r}, {self.factory!r}, {self.widget!r})"

    def build(self):
        """This will create the initial list of widgets."""
        if self.widget is None:
            self.widget = self.create(data={}, style={})

    def get_widgets(self) -> List[abc.Child]:
        if self.widget is None:
            return []

        else:
            return [self.widget]


class ListWidgetBuilder(WidgetBuilder, abc.ListWidgetBuilder):
    """"""
    key: str
    iterable: DynamicList
    widgets: List[abc.Child]

    def __init__(self, parent: abc.Parent, factory: Type[abc.Child]):
        super().__init__(parent, factory)
        self.key, self.iterable = self.factory.get_iterable_info(data=parent.data)
        self.widgets: List[abc.Child] = []

        self.on(name=":append", emitter=self.iterable, function=self.on_model_append)
        self.on(name=":remove", emitter=self.iterable, function=self.on_model_remove)
        self.on(name=":insert", emitter=self.iterable, function=self.on_model_insert)
        self.on(name=":pop", emitter=self.iterable, function=self.on_model_pop)

        self.build()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.parent!r}, {self.factory!r}, {self.widgets!r})"

    def build(self):
        """This will build widgets so they fit the iterable."""
        elements = self.iterable

        if len(elements) > len(self.widgets):
            # we should create new widgets.
            for index in range(len(self.widgets), len(elements)):
                self.local_append(index=index)

        elif len(elements) < len(self.widgets):
            # we should remove widgets.
            for index in reversed(list(range(len(elements), len(self.widgets)))):
                self.local_remove(index)

    def get_widgets(self) -> List[abc.Child]:
        return self.widgets

    def create_at(self, index: int) -> abc.Child:
        element = self.iterable[index]

        if not isinstance(element, Emitter):
            element = DynamicListItem(data=self.iterable, index=index)

        return self.create(data={'index': index, self.key: element}, style={})

    def update_parent(self):
        self.parent.update()

    def on_model_append(self, event: Event) -> None:
        if self.should_build():
            self.local_append(index=event.kwargs['index'])
            self.update_parent()

    def on_model_remove(self, event: Event) -> None:
        if self.should_build():
            self.local_remove(index=event.kwargs['index'])
            self.update_parent()

    def on_model_insert(self, event: Event) -> None:
        if self.should_build():
            self.local_insert(index=event.kwargs['index'])
            self.update_parent()

    def on_model_pop(self, event: Event) -> None:
        if self.should_build():
            self.local_insert(index=event.kwargs['index'])
            self.update_parent()

    def local_append(self, index: int) -> None:
        widget = self.create_at(index)
        self.widgets.append(widget)

    def local_remove(self, index: int) -> None:
        raise NotImplementedError("TODO")
        # widget = self.widgets.pop(index)
        # widget.grid_forget()
        # widget.destroy()

    def local_insert(self, index: int) -> None:
        raise NotImplementedError("TODO")
        # widget = self.create_at(index)
        # self.widgets.insert(index, widget)

    def local_pop(self, index: int) -> None:
        raise NotImplementedError("TODO")
        # widget = self.widgets.pop(index)
        # widget.grid_forget()
        # widget.destroy()


def widget_builder_factory(parent: abc.Parent, factory: Type[abc.Child]) -> WidgetBuilder:
    """Create a ChildrenBuilder depending on the configuration of `cls`"""

    if factory.is_iterable():
        builder = ListWidgetBuilder(parent=parent, factory=factory)

    else:
        builder = UnitWidgetBuilder(parent=parent, factory=factory)

    return builder


class GridManager(abc.GridManager):
    _grid_method: ClassVar[Optional[Callable[[abc.Child, List[abc.Child], dict], None]]]
    _grid_padx: ClassVar[int]
    _grid_pady: ClassVar[int]

    @classmethod
    def _init_grid_method(cls) -> Callable[[], None]:
        if issubclass(cls, Horizontal):
            if issubclass(cls, Centered):
                return grid_centered_horizontally

            else:
                return grid_horizontally

        elif issubclass(cls, Vertical):
            if issubclass(cls, Centered):
                return grid_centered_vertically

            else:
                return grid_vertically

        else:
            raise Exception(f"{cls.__name__} must implement Vertical | Horizontal")

    @classmethod
    def _init_grid_manager_class(cls, kwargs: dict):
        cls._grid_method = cls._init_grid_method()

        assert cls._grid_method is None or hasattr(cls._grid_method, '__call__')

        padding = _get_class_attr(cls, 'PADDING', kwargs, default=(0, 0))

        if isinstance(padding, int):
            cls._grid_padx = cls._grid_pady = padding

        elif isinstance(padding, tuple) and len(padding) == 2 and all(isinstance(arg, int) for arg in padding):
            cls._grid_padx, cls._grid_pady = padding

        else:
            raise TypeError(f"{cls.__name__}.PADDING should be int | Tuple[int, int] not {padding!r}.")

    def grid_widgets(self, widgets: List[abc.Child]):
        config = dict(sticky=tk.NSEW, padx=self._grid_padx, pady=self._grid_pady)

        self.__class__._grid_method(parent=self, widgets=widgets, config=config)


class Parent(GridManager, abc.Parent):
    _children_factories: ClassVar[List[Type[abc.Child]]]

    builders: List[abc.WidgetBuilder]
    widgets: List[abc.Child]

    @classmethod
    def _init_parent_class(cls, kwargs: dict):
        cls._init_grid_manager_class(kwargs)
        cls._init_has_style_and_data_class(kwargs)

        factories = _get_class_attr(cls, '_factories', {}, default=[])

        cls._children_factories = factories + [
            factory
            for factory in cls.__dict__.values()
            if isinstance(factory, (type, ABCMeta))
            if issubclass(factory, abc.Child)
        ]

        assert isinstance(cls._children_factories, list)

    def __init__(self, data: dict = None, parent_data: DynamicData = None,
                 style: dict = None, parent_style: DynamicStyle = None):
        HasStyleAndData.__init__(self, data=data, parent_data=parent_data, style=style, parent_style=parent_style)
        GridManager.__init__(self)

        self.builders = [widget_builder_factory(parent=self, factory=factory) for factory in self._children_factories]

        self.widgets = []

        self.update_widgets()

    def update_widgets(self):
        self.widgets = [widget for builder in self.builders for widget in builder.get_widgets()]
        self.grid_widgets(self.widgets)


class Child(abc.Child):
    @classmethod
    def _init_child_class(cls, kwargs: dict):
        cls._init_has_logic_class(kwargs)
        cls._init_can_iter_class(kwargs)

    def __init__(self, parent: abc.Parent = None):
        self.parent: Optional[abc.Parent] = parent
        HasLogic.__init__(self)
        HasIter.__init__(self)


class Tree(HasValue, Child, Parent):
    @classmethod
    def _init_tree_class(cls, kwargs: dict):
        cls._init_parent_class(kwargs)
        cls._init_child_class(kwargs)
        cls._init_has_value_class(kwargs)

    def __init__(self, parent: abc.Parent = None, data: dict = None, style: dict = None):
        Child.__init__(self, parent=parent)

        if self.parent is None:
            parent_data = None
            parent_style = None

        else:
            parent_data = self.parent.data
            parent_style = self.parent.style

        Parent.__init__(self, data=data, parent_data=parent_data, style=style, parent_style=parent_style)

        HasValue.__init__(self, parent_data=parent_data)

        self.update_style()

    def update(self):
        self.update_widgets()

        for child in self.widgets:
            child.update()
