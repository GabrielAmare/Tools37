import logging
from typing import Optional, ClassVar, List
from typing import Tuple

from . import abc
from .ComponentConfig import ComponentConfig
from .builders import WidgetBuilder
from .events import Observer, Event
from ..dynamic import Dynamic, DynamicData, DynamicStyle, view, DynamicDict, DynamicList, DynamicBinder
from ..evaluable import evaluate, Evaluable, EvaluablePath

__all__ = ['Component']


class Component(abc.Component):
    __config__: ClassVar[ComponentConfig]

    style: DynamicStyle
    data: DynamicData
    binder: Optional[DynamicBinder]

    builders: List[abc.WidgetBuilder]
    widgets: List[abc.Component]

    @classmethod
    def is_iterable(cls) -> bool:
        return cls.__config__.is_iterable()

    @classmethod
    def get_iterable_info(cls, data: DynamicData) -> Tuple[str, DynamicList]:
        return cls.__config__.get_iterable_info(data)

    @classmethod
    def evaluate_condition(cls, data: DynamicDict) -> bool:
        return cls.__config__.evaluate_condition(data)

    @classmethod
    def get_condition_paths(cls) -> List[EvaluablePath]:
        try:
            return cls.__config__.get_condition_paths()

        except TypeError:
            return []

    def _init_style(self, local: dict = None):
        style = {}

        if local:
            style.update(local)

        if self.__config__.style_factory:
            style.update(self.__config__.style_factory(self))

        parent_style = self.parent.style if isinstance(self.parent, Component) else None

        if not style and isinstance(parent_style, DynamicStyle):
            return self.parent.style

        else:
            return DynamicStyle(style, parent_style)

    def _init_data(self, local: dict = None):
        data = {}

        if local:
            data.update(local)

        if self.__config__.data_factory:
            data.update(self.__config__.data_factory(self))

        parent_data = self.parent.data if isinstance(self.parent, Component) else None

        if not data and isinstance(parent_data, DynamicData):
            return self.parent.data

        else:
            return DynamicData(data, parent_data)

    def _init_binder(self):
        if isinstance(self.__config__.binder, Evaluable):
            if isinstance(self.parent, Component):
                return DynamicBinder.from_evaluable(evaluable=self.__config__.binder, data=self.parent.data)

            else:
                logging.warning(f"Cannot defined {self.__class__.__name__}.binder")

        return None

    def _init_builders(self):
        return [WidgetBuilder.make(parent=self, factory=factory) for factory in self.__config__.widgets_factory]

    @classmethod
    def _init_component_class(cls, kwargs: dict) -> None:
        cls.__config__ = ComponentConfig.from_component_class(component_cls=cls, kwargs=kwargs)

    def __init__(self, parent: abc.Component = None, data: dict = None, style: dict = None):
        self.parent: Optional[abc.Component] = parent

        self.style = self._init_style(local=style)
        self.data = self._init_data(local=data)
        self.binder = self._init_binder()
        self.builders = self._init_builders()

        self.update_style()

        self.widgets = []
        self.update_widgets()

        self._setup_events()

    def _setup_events(self) -> None:
        if isinstance(self.binder, DynamicBinder):
            Observer().on(name=f".{self.__config__.binder!s}", emitter=self.data, function=self._update_local)

        for key, value in self.style.items():
            if isinstance(value, Evaluable):
                self.style.on(name='*', emitter=self.data, function=self.update_style)

    def update_data(self):
        if isinstance(self.binder, DynamicBinder):
            self._update_local()

        for widget in self.widgets:
            widget.update_data()

    def update_style(self, _: Event = None) -> None:
        data_view = self.data.view()
        style_view = self.style.view()
        valid_keys = self.keys()

        # CREATE VIEW
        style = {}
        for key, value in style_view.items():
            if key in valid_keys:
                value = evaluate(value, data_view)
                value = view(value)
                style[key] = value

        # CHECK INTEGRITY
        assert isinstance(style, dict)
        for key, value in style.items():
            assert isinstance(key, str)
            if isinstance(value, (Evaluable, Dynamic)):
                raise Exception(f"Style error : {key!s}={value!r} should not be Evaluable | Dynamic")

        self.config(**style)

    def update_widgets(self):
        self.widgets = [widget for builder in self.builders for widget in builder.get_widgets()]
        self.__config__.grid_method(parent=self, widgets=self.widgets)

    def update(self):
        self.update_widgets()

        for widget in self.widgets:
            widget.update()

    def _set_local(self, value):
        """Set the local value for the widget."""
        raise Exception(f"Method {self.__class__.__name__}._set_local undefined !")

    def _get_local(self):
        """Get the local value of the widget."""
        raise Exception(f"Method {self.__class__.__name__}._get_local undefined !")

    def _update_local(self, *_, **__):
        assert isinstance(self.binder, DynamicBinder)
        self._set_local(value=self.binder.view())

    def _update_model(self, *_, **__):
        assert isinstance(self.binder, DynamicBinder)
        self.binder.set(value=self._get_local())
