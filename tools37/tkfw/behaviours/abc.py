from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, Callable, Optional, Union, Tuple, List

from ..dynamic import DynamicData, DynamicStyle, DynamicList, DynamicGetter, DynamicSetter
from ..evaluable import Evaluable, EvaluablePath

__all__ = [
    'HasStyle',
    'HasData',
    'HasStyleAndData',
    'HasIter',
    'HasLogic',
    'HasValue'
]


class HasStyle(ABC):
    _style_factory: ClassVar[Optional[Callable[[HasStyle], dict]]]
    style: DynamicStyle

    @classmethod
    @abstractmethod
    def _init_has_style_class(cls, kwargs: dict):
        """"""

    @abstractmethod
    def __init__(self, style: dict = None, parent_style: DynamicStyle = None):
        """"""


class HasData(ABC):
    _data_factory: ClassVar[Optional[Callable[[HasData], dict]]]
    data: DynamicData

    @classmethod
    @abstractmethod
    def _init_has_data_class(cls, kwargs: dict) -> None:
        """"""

    @abstractmethod
    def __init__(self, data: dict = None, parent_data: DynamicData = None):
        """"""


class HasStyleAndData(HasStyle, HasData, ABC):
    @classmethod
    @abstractmethod
    def _init_has_style_and_data_class(cls, kwargs: dict):
        """"""

    @abstractmethod
    def __init__(self, data: dict = None, parent_data: DynamicData = None,
                 style: dict = None, parent_style: DynamicStyle = None):
        """"""

    @abstractmethod
    def _register_style_events(self) -> None:
        """"""

    @abstractmethod
    def update_style(self) -> None:
        """"""

    @abstractmethod
    def render_style(self) -> dict:
        """"""


class HasIter(ABC):
    _iterable_key: ClassVar[Optional[str]]
    _iterable: ClassVar[Optional[Evaluable]]

    @classmethod
    @abstractmethod
    def _init_can_iter_class(cls, kwargs: dict) -> None:
        """"""

    @classmethod
    @abstractmethod
    def is_iterable(cls) -> bool:
        """"""

    @classmethod
    @abstractmethod
    def get_iterable_info(cls, data: DynamicData) -> Tuple[str, DynamicList]:
        """"""


class HasLogic(ABC):
    _condition: ClassVar[Union[bool, Evaluable]]

    @classmethod
    @abstractmethod
    def _init_has_logic_class(cls, kwargs: dict) -> None:
        """"""

    @classmethod
    @abstractmethod
    def evaluate_condition(cls, data: DynamicData) -> bool:
        """Return True if the class condition is fulfilled by the given data."""

    @classmethod
    @abstractmethod
    def get_condition_paths(cls) -> List[EvaluablePath]:
        """Return all the EvaluablePath that the class condition rely on."""


class HasValue(ABC):
    __setter__: ClassVar[Optional[Evaluable]]
    __getter__: ClassVar[Optional[Evaluable]]

    get_model: Optional[DynamicGetter]
    set_model: Optional[DynamicSetter]

    @classmethod
    @abstractmethod
    def _init_has_value_class(cls, kwargs: dict):
        """"""

    @abstractmethod
    def __init__(self, parent_data: DynamicData = None):
        """"""

    def _set_local(self, value):
        """Set the local value for the widget."""

    def _get_local(self):
        """Get the local value of the widget."""
