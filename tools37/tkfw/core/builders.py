from abc import ABC
from typing import Optional, List, Type

from .abc import Component
from . import abc
from ..dynamic import DynamicList, DynamicListItem
from .events import Observer, Event

__all__ = [
    'WidgetBuilder',
    'ListWidgetBuilder',
    'UnitWidgetBuilder'
]


def _del_widget(widget: Component) -> None:
    widget.grid_forget()
    widget.destroy()


class WidgetBuilder(Observer, abc.WidgetBuilder, ABC):
    @staticmethod
    def make(parent: Component, factory: Type[Component]) -> abc.WidgetBuilder:
        """Create a ChildrenBuilder depending on the configuration of `cls`"""
        cls = ListWidgetBuilder if factory.is_iterable() else UnitWidgetBuilder
        return cls(parent=parent, factory=factory)

    def __init__(self, parent: Component, factory: Type[Component]):
        self.parent: Component = parent
        self.factory: Type[Component] = factory

        for path in self.factory.get_condition_paths():
            self.on(name=f".{path!s}", emitter=self.parent.data, function=self.rebuild)

    def rebuild(self, _: Event = None):
        self.build()
        self.update_parent()

    def update_parent(self):
        self.parent.update()

    def create(self, data: dict = None, style: dict = None) -> Component:
        return self.factory(parent=self.parent, data=data, style=style)

    def should_build(self) -> bool:
        return self.factory.evaluate_condition(data=self.parent.data)


class UnitWidgetBuilder(WidgetBuilder):
    """"""
    widget: Optional[Component]

    def __init__(self, parent: Component, factory: Type[Component]):
        super().__init__(parent, factory)
        self.widget: Optional[Component] = None

        self.build()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.parent!r}, {self.factory!r}, {self.widget!r})"

    def build(self):
        """This will create the initial list of widgets."""
        if self.should_build():
            if self.widget is None:
                self.widget = self.create(data={}, style={})
        else:
            self.del_widgets()

    def get_widgets(self) -> List[Component]:
        if self.widget is None:
            return []

        else:
            return [self.widget]

    def del_widgets(self) -> None:
        if self.widget is not None:
            _del_widget(self.widget)
            self.widget = None


class ListWidgetBuilder(WidgetBuilder):
    """"""
    key: str
    iterable: DynamicList
    widgets: List[Component]

    def __init__(self, parent: Component, factory: Type[Component]):
        super().__init__(parent, factory)
        self.key, self.iterable = self.factory.get_iterable_info(data=parent.data)
        self.widgets: List[Component] = []

        self.on(name=":append", emitter=self.iterable, function=self.on_model_append)
        self.on(name=":remove", emitter=self.iterable, function=self.on_model_remove)
        self.on(name=":insert", emitter=self.iterable, function=self.on_model_insert)
        self.on(name=":pop", emitter=self.iterable, function=self.on_model_pop)

        self.build()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.parent!r}, {self.factory!r}, {self.widgets!r})"

    def build(self):
        """This will build widgets so they fit the iterable."""
        if self.should_build():
            elements = self.iterable

        else:
            elements = []

        if len(elements) > len(self.widgets):
            # we should create new widgets.
            for index in range(len(self.widgets), len(elements)):
                self.local_append(index=index)

        elif len(elements) < len(self.widgets):
            # we should remove widgets.
            for index in reversed(list(range(len(elements), len(self.widgets)))):
                self.local_remove(index)

    def get_widgets(self) -> List[Component]:
        return self.widgets

    def del_widgets(self) -> None:
        for widget in self.widgets:
            _del_widget(widget)

        self.widgets = []

    def create_at(self, index: int) -> Component:
        element = DynamicListItem(data=self.iterable, index=index)

        # if not isinstance(element, Emitter):
        #     element = DynamicListItem(data=self.iterable, index=index)
        #

        return self.create(data={'index': index, self.key: element}, style={})

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
            self.local_pop(index=event.kwargs['index'])
            self.update_parent()

    def local_append(self, index: int) -> None:
        widget = self.create_at(index)
        self.widgets.append(widget)

    def _destroy_last_widget(self) -> None:
        widget = self.widgets.pop(-1)
        _del_widget(widget)

    def _update_widgets_after(self, index: int) -> None:
        for delta, widget in enumerate(self.widgets[index:]):
            new_index = index + delta
            # TODO: fix this issue !
            widget.data['index'] = new_index
            element = widget.data[self.key]
            if isinstance(element, DynamicListItem):
                element.update(index=new_index)

            widget.update_data()

    def local_remove(self, index: int) -> None:
        self._destroy_last_widget()
        self._update_widgets_after(index)

    def local_insert(self, index: int) -> None:
        self.create_at(index=len(self.iterable) - 1)  # TODO: check it's working
        self._update_widgets_after(index)

    def local_pop(self, index: int) -> None:
        self._destroy_last_widget()
        self._update_widgets_after(index)
