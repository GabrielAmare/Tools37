import logging
from abc import ABCMeta
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Callable, List, Type, Tuple

from .GridMethod import GridCenteredVertically, GridCenteredHorizontally, GridVertically, GridHorizontally
from .abc import ComponentConfig, Component, GridMethod
from .utils import Vertical, Horizontal, Centered
from ..dynamic import DynamicData, DynamicDict, DynamicList
from ..evaluable import as_evaluable_path, EvaluablePath, EvaluableBinder, Evaluable, EvaluableExpression, \
    as_evaluable_expression

__all__ = [
    'ComponentConfig'
]


class Keys(str, Enum):
    WIDGETS_FACTORY = 'widgets_factory'
    STYLE_FACTORY = 'style_factory'
    STYLE = 'STYLE'
    DATA_FACTORY = 'data_factory'
    DATA = 'DATA'
    FOR = 'FOR'
    IN = 'IN'
    IF = 'IF'
    BINDER = 'BIND'
    GRID_CONFIG = 'GRID'


def _error(component_cls: Type[Component], key: str, types: List[type]) -> TypeError:
    return TypeError(f"{component_cls.__name__}.{key} should be {' | '.join(t.__name__ for t in types)}.")


@dataclass
class ComponentConfig(ComponentConfig):
    style_factory: Optional[Callable[[Component], dict]]
    data_factory: Optional[Callable[[Component], dict]]
    iterable_key: str
    iterable: Optional[EvaluablePath]
    condition: Optional[Evaluable]
    binder: Optional[EvaluableBinder]
    grid_method: GridMethod
    widgets_factory: List[Type[Component]]

    @staticmethod
    def _get_style_factory(cls, kwargs: dict):
        if Keys.STYLE_FACTORY in kwargs:
            return kwargs[Keys.STYLE_FACTORY]

        elif Keys.STYLE_FACTORY in cls.__dict__:
            return getattr(cls, Keys.STYLE_FACTORY)

        elif Keys.STYLE in cls.__dict__:
            base_dict = getattr(cls, Keys.STYLE)

            return lambda _: base_dict.copy()

        else:
            return None

    @staticmethod
    def _get_data_factory(cls, kwargs: dict):
        if Keys.DATA_FACTORY in kwargs:
            return kwargs[Keys.DATA_FACTORY]

        elif Keys.DATA_FACTORY in cls.__dict__:
            return getattr(cls, Keys.DATA_FACTORY)

        elif Keys.DATA in cls.__dict__:
            base_dict = getattr(cls, Keys.DATA)

            return lambda _: base_dict.copy()

        else:
            return None

    @staticmethod
    def _get_iterable(cls, kwargs: dict):
        value = kwargs.get(Keys.IN, None)

        if value is None:
            return None

        elif isinstance(value, EvaluablePath):
            return value

        elif isinstance(value, str):
            return as_evaluable_path(value)

        else:
            raise _error(component_cls=cls, key=Keys.IN, types=[type(None), EvaluablePath, str])

    @staticmethod
    def _get_iterable_key(cls, kwargs: dict):
        value = kwargs.get(Keys.FOR, None)

        if value is None:
            return ''

        elif isinstance(value, str):
            return value

        else:
            raise _error(component_cls=cls, key=Keys.FOR, types=[type(None), str])

    @staticmethod
    def _get_condition(cls, kwargs: dict):
        value = kwargs.get(Keys.IF, None)

        if value is None:
            return None

        elif isinstance(value, EvaluableExpression):
            return value

        elif isinstance(value, str):
            return as_evaluable_expression(expr=value)

        else:
            raise _error(component_cls=cls, key=Keys.IF, types=[type(None), EvaluableExpression, str])

    @staticmethod
    def _get_binder(cls, kwargs: dict):
        value = kwargs.get(Keys.BINDER, None)

        if value is None:
            return None

        elif isinstance(value, str):
            return as_evaluable_path(path=value)

        else:
            raise _error(component_cls=cls, key=Keys.BINDER, types=[type(None), str])

    @staticmethod
    def _get_grid_method(cls):
        if issubclass(cls, Horizontal):
            if issubclass(cls, Centered):
                return GridCenteredHorizontally

            else:
                return GridHorizontally

        elif issubclass(cls, Vertical):
            if issubclass(cls, Centered):
                return GridCenteredVertically

            else:
                return GridVertically

        else:
            return GridVertically
            # raise Exception(f"{cls.__name__} must implement Vertical | Horizontal")

    @staticmethod
    def _get_grid_config(cls, kwargs: dict):
        value = kwargs.get(Keys.GRID_CONFIG, None)

        if value is None:
            return dict(sticky='nsew')

        elif isinstance(value, dict):
            return value

        else:
            raise _error(component_cls=cls, key=Keys.GRID_CONFIG, types=[type(None), dict])

    @staticmethod
    def _get_widgets_factory(cls, kwargs: dict):
        if Keys.WIDGETS_FACTORY in kwargs:
            factories = kwargs[Keys.WIDGETS_FACTORY]

        elif Keys.WIDGETS_FACTORY in cls.__dict__:
            factories = cls.__dict__[Keys.WIDGETS_FACTORY]

        else:
            factories = []

        return factories + [
            factory
            for factory in cls.__dict__.values()
            if isinstance(factory, (type, ABCMeta))
            if issubclass(factory, Component)
        ]

    @classmethod
    def from_component_class(cls, component_cls: Type[Component], kwargs: dict):
        return cls(
            style_factory=cls._get_style_factory(component_cls, kwargs),
            data_factory=cls._get_data_factory(component_cls, kwargs),
            iterable=cls._get_iterable(component_cls, kwargs),
            iterable_key=cls._get_iterable_key(component_cls, kwargs),
            condition=cls._get_condition(component_cls, kwargs),
            binder=cls._get_binder(component_cls, kwargs),
            grid_method=cls._get_grid_method(component_cls)(cls._get_grid_config(component_cls, kwargs)),
            widgets_factory=cls._get_widgets_factory(component_cls, kwargs)
        )

    def is_iterable(self) -> bool:
        return isinstance(self.iterable, EvaluablePath)

    def get_iterable_info(self, data: DynamicData) -> Tuple[str, DynamicList]:
        assert isinstance(self.iterable_key, str)
        assert isinstance(self.iterable, EvaluablePath)

        return self.iterable_key, self.iterable.get(data)

    def evaluate_condition(self, data: DynamicDict) -> bool:
        """Return True if the class condition is fulfilled by the given data."""
        condition = self.condition

        if self.condition is None:
            return True

        elif isinstance(self.condition, Evaluable):
            return bool(self.condition.evaluate(data=data.view()))

        else:
            logging.warning(f"{self.__class__.__name__}.{Keys.IF} invalid type {type(condition).__name__!r}.")
            return False

    def get_condition_paths(self) -> List[EvaluablePath]:
        if isinstance(self.condition, bool):
            return []

        elif isinstance(self.condition, EvaluableExpression):
            return self.condition.get_paths()

        else:
            raise TypeError(self.condition)
