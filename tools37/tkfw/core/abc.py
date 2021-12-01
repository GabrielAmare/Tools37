from __future__ import annotations

from abc import ABC, abstractmethod
from tkinter import Grid, Misc
from typing import List, ClassVar, Optional, Callable, Type, Tuple

from ..dynamic import DynamicData, DynamicStyle, DynamicBinder, DynamicDict, DynamicList
from ..evaluable import EvaluablePath, Evaluable, EvaluableBinder

__all__ = [
    'ComponentConfig',
    'Component',
    'GridMethod',
    'WidgetBuilder'
]


class ComponentConfig(ABC):
    style_factory: Optional[Callable[[Component], dict]]
    data_factory: Optional[Callable[[Component], dict]]
    iterable_key: str
    iterable: Optional[EvaluablePath]
    condition: Optional[Evaluable]
    binder: Optional[EvaluableBinder]
    grid_method: GridMethod
    widgets_factory: List[Type[Component]]

    @abstractmethod
    def is_iterable(self) -> bool:
        """"""

    @abstractmethod
    def get_iterable_info(self, data: DynamicData) -> Tuple[str, DynamicList]:
        """"""

    @abstractmethod
    def evaluate_condition(self, data: DynamicDict) -> bool:
        """Return True if the class condition is fulfilled by the given data."""

    @abstractmethod
    def get_condition_paths(self) -> List[EvaluablePath]:
        """"""


class Component(Misc, Grid, ABC):
    __config__: ClassVar[ComponentConfig]

    style: DynamicStyle
    data: DynamicData
    binder: Optional[DynamicBinder]

    builders: List[WidgetBuilder]
    widgets: List[Component]

    @classmethod
    @abstractmethod
    def is_iterable(cls) -> bool:
        """"""

    @classmethod
    @abstractmethod
    def evaluate_condition(cls, data: DynamicDict) -> bool:
        """"""

    @classmethod
    @abstractmethod
    def get_condition_paths(cls) -> List[EvaluablePath]:
        """"""

    @classmethod
    @abstractmethod
    def get_iterable_info(cls, data: DynamicData) -> Tuple[str, DynamicList]:
        """"""

    @abstractmethod
    def __init__(self, parent: Component = None, data: dict = None, style: dict = None):
        """"""

    @abstractmethod
    def update(self):
        """"""

    @abstractmethod
    def update_data(self):
        """"""


class GridMethod(ABC):
    @abstractmethod
    def __init__(self, config: dict):
        """"""

    @abstractmethod
    def __call__(self, parent: Component, widgets: List[Component]):
        """"""


class WidgetBuilder(ABC):
    parent: Component
    factory: Type[Component]

    @abstractmethod
    def __init__(self, parent: Component, factory: Type[Component]):
        """"""

    @abstractmethod
    def create(self, data: dict = None, style: dict = None) -> Component:
        """"""

    @abstractmethod
    def should_build(self) -> bool:
        """"""

    @abstractmethod
    def build(self):
        """"""

    @abstractmethod
    def get_widgets(self) -> List[Component]:
        """"""

    @abstractmethod
    def del_widgets(self) -> None:
        """"""
