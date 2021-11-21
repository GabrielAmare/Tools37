from __future__ import annotations

from abc import ABC, abstractmethod
from tkinter import Misc, Grid
from typing import ClassVar, Callable, Optional, List, Type

from ..behaviours import HasLogic, HasIter, HasStyleAndData
from ..dynamic import DynamicData, DynamicList
from ..events import Emitter, Event


class WidgetBuilder(ABC):
    parent: Parent
    factory: Type[Child]

    @abstractmethod
    def __init__(self, parent: Parent, factory: Type[Child]):
        """"""

    @abstractmethod
    def create(self, data: dict = None, style: dict = None) -> Child:
        """"""

    @abstractmethod
    def should_build(self) -> bool:
        """"""

    @abstractmethod
    def build(self):
        """"""

    @abstractmethod
    def get_widgets(self) -> List[Child]:
        """"""


class UnitWidgetBuilder(WidgetBuilder, ABC):
    widget: Optional[Child]


class ListWidgetBuilder(WidgetBuilder, ABC):
    key: str
    iterable: DynamicList
    widgets: List[Child]

    @abstractmethod
    def create_at(self, index: int) -> Child:
        """"""

    @abstractmethod
    def local_append(self, index: int) -> None:
        """"""

    @abstractmethod
    def local_remove(self, index: int) -> None:
        """"""

    @abstractmethod
    def local_insert(self, index: int) -> None:
        """"""

    @abstractmethod
    def local_pop(self, index: int) -> None:
        """"""

    @abstractmethod
    def on_model_append(self, event: Event) -> None:
        """"""

    @abstractmethod
    def on_model_remove(self, event: Event) -> None:
        """"""

    @abstractmethod
    def on_model_insert(self, event: Event) -> None:
        """"""

    @abstractmethod
    def on_model_pop(self, event: Event) -> None:
        """"""


class ChildrenFactory(Emitter):
    """This class handle the build for a specific tree type into a specified parent tree."""

    parent: Parent
    factory: Type[Child]
    children: List[Child]

    @abstractmethod
    def __init__(self, parent: Parent, factory: Type[Child]):
        """"""

    @abstractmethod
    def _create(self, data: dict = None, style: dict = None) -> Child:
        """"""

    @abstractmethod
    def _create_list_item(self, index: int) -> Child:
        """"""

    ####################################################################################################################
    # CHILDREN UPDATES ON EVENTS
    ####################################################################################################################

    @abstractmethod
    def append(self, event: Event) -> None:
        """"""

    @abstractmethod
    def insert(self, event: Event) -> None:
        """"""

    @abstractmethod
    def remove(self, event: Event) -> None:
        """"""

    @abstractmethod
    def build(self, data: DynamicData) -> List[Child]:
        """"""


class Component(Misc, Grid, ABC):  # TODO: may (or not) add -> HasData & HasStyle
    pass


class GridManager(ABC):
    _grid_method: ClassVar[Optional[Callable[[Child, List[Child], dict], None]]]
    _grid_padx: ClassVar[int]
    _grid_pady: ClassVar[int]

    @classmethod
    @abstractmethod
    def _init_grid_method(cls) -> Callable[[], None]:
        """"""

    @classmethod
    @abstractmethod
    def _init_grid_manager_class(cls, kwargs: dict) -> None:
        """"""

    @abstractmethod
    def grid_widgets(self, widgets: List[Child]) -> None:
        """This method will grid the childs."""


class Parent(HasStyleAndData, Component, ABC):
    _children_factories: ClassVar[List[Type[Child]]]

    builders: List[ChildrenFactory]
    widgets: List[Child]

    @classmethod
    @abstractmethod
    def _init_parent_class(cls, kwargs: dict):
        """"""


class Child(HasLogic, HasIter, Component, ABC):
    @abstractmethod
    def __init__(self, parent: Parent, data: dict = None, style: dict = None):
        """"""


class Tree(ABC):
    pass
