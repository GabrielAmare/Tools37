import tkinter as tk
from enum import Enum
from typing import Optional, ClassVar, Callable, Union, Tuple, List

from . import abc
from ..console import console
from ..dynamic import view, Dynamic, DynamicStyle, DynamicData, DynamicDict, DynamicList, DynamicSetter, DynamicGetter
from ..evaluable import evaluate, Evaluable, EvaluableSetter, EvaluableGetter, EvaluablePath, as_evaluable_path, \
    as_evaluable_expression, EvaluableExpression
from ..events import Observer, Event
from ..functions import init_from_factory

__all__ = [
    'Keys',
    'HasStyle',
    'HasData',
    'HasIter',
    'HasLogic',
    'HasValue',
    'HasStyleAndData'
]


class Keys(str, Enum):
    STYLE_FACTORY = 'style_factory'
    STYLE = 'STYLE'
    DATA_FACTORY = 'data_factory'
    DATA = 'DATA'
    FOR = 'FOR'
    IN = 'IN'
    IF = 'IF'
    GETTER = 'GET'
    SETTER = 'SET'
    BINDER = 'BIND'


def pop_attr(__object: object, __key: str):
    value = getattr(__object, __key)
    delattr(__object, __key)
    return value


def _init_factory(factory_key, dict_key, default):
    def wrapped(cls, kwargs):
        if factory_key in kwargs:
            value = kwargs[factory_key]

        elif factory_key in cls.__dict__:
            value = pop_attr(cls, factory_key)

        elif dict_key in cls.__dict__:
            base_dict = pop_attr(cls, dict_key)

            def value(_=None):
                return base_dict.copy()

        else:
            value = default

        return value

    return wrapped


def _check_style_render_integrity(style: dict):
    assert isinstance(style, dict)
    for key, value in style.items():
        assert isinstance(key, str)
        if isinstance(value, (Evaluable, Dynamic)):
            raise Exception(f"Style error : {key!s}={value!r} should not be Evaluable | Dynamic")


_init_style_factory = _init_factory(factory_key=Keys.STYLE_FACTORY, dict_key=Keys.STYLE, default=None)
_init_data_factory = _init_factory(factory_key=Keys.DATA_FACTORY, dict_key=Keys.DATA, default=None)


class HasStyle(abc.HasStyle):
    _style_factory: ClassVar[Optional[Callable[[abc.HasStyle], dict]]]
    style: DynamicStyle

    @classmethod
    def _init_has_style_class(cls, kwargs: dict):
        cls._style_factory = _init_style_factory(cls, kwargs)

    def __init__(self, style: dict = None, parent_style: DynamicStyle = None):
        self.style = init_from_factory(
            factory=DynamicStyle,
            parent=parent_style,
            dict_local=style,
            dict_factory=self._style_factory
        )


class HasData(abc.HasData):
    _data_factory: ClassVar[Optional[Callable[[abc.HasData], dict]]]
    data: DynamicData

    @classmethod
    def _init_has_data_class(cls, kwargs: dict) -> None:
        cls._data_factory = _init_data_factory(cls, kwargs)

    def __init__(self, data: dict = None, parent_data: DynamicData = None):
        self.data = init_from_factory(
            factory=DynamicData,
            parent=parent_data,
            dict_local=data,
            dict_factory=self._data_factory
        )


class HasIter(abc.HasIter):
    _iterable_key: ClassVar[Optional[str]]
    _iterable: ClassVar[Optional[EvaluablePath]]

    @classmethod
    def _init_iterable(cls, kwargs: dict):
        _iterable = kwargs.get(Keys.IN, None)

        if isinstance(_iterable, str):
            cls._iterable = as_evaluable_path(_iterable)

        elif isinstance(_iterable, EvaluablePath):
            cls._iterable = _iterable

        elif _iterable is None:
            cls._iterable = _iterable

        else:
            raise TypeError(f"{cls.__name__}._iterable should be None | str | Path.")

    @classmethod
    def _init_iterable_key(cls, kwargs: dict):
        _iterable_key = kwargs.get(Keys.FOR, None)

        if isinstance(_iterable_key, str):
            cls._iterable_key = _iterable_key

        elif _iterable_key is None:
            cls._iterable_key = None

        else:
            raise TypeError(f"{cls.__name__}._iterable_key should be None | str")

    @classmethod
    def _init_can_iter_class(cls, kwargs: dict) -> None:
        cls._init_iterable(kwargs)
        cls._init_iterable_key(kwargs)

        if cls._iterable is not None and cls._iterable_key is None:
            raise Exception(f"{cls.__name__}.{Keys.IN} is defined, so {cls.__name__}.{Keys.FOR} should be too.")

    @classmethod
    def is_iterable(cls) -> bool:
        return isinstance(cls._iterable, EvaluablePath)

    @classmethod
    def get_iterable_info(cls, data: DynamicData) -> Tuple[str, DynamicList]:
        assert isinstance(cls._iterable_key, str)
        assert isinstance(cls._iterable, EvaluablePath)

        return cls._iterable_key, cls._iterable.get(data)


class HasLogic(abc.HasLogic):
    _condition: ClassVar[Union[bool, Evaluable]]

    @classmethod
    def _init_has_logic_class(cls, kwargs: dict) -> None:
        _condition = kwargs.get(Keys.IF, True)

        if isinstance(_condition, bool):
            cls._condition = _condition

        elif isinstance(_condition, str):
            cls._condition = as_evaluable_expression(expr=_condition)

        else:
            raise TypeError(f"{cls.__name__}.__if__ should be bool | EvaluableBoolean.")

    @classmethod
    def evaluate_condition(cls, data: DynamicDict) -> bool:
        """Return True if the class condition is fulfilled by the given data."""
        condition = cls._condition

        if isinstance(cls._condition, bool):
            return cls._condition

        elif isinstance(cls._condition, Evaluable):
            return bool(cls._condition.evaluate(data=data.view()))

        else:
            console.warning(f"{cls.__name__}.__if__ invalid type {type(condition).__name__!r}.")
            return False

    @classmethod
    def get_condition_paths(cls) -> List[EvaluablePath]:
        if isinstance(cls._condition, bool):
            return []

        elif isinstance(cls._condition, EvaluableExpression):
            return cls._condition.get_paths()

        else:
            raise TypeError(cls._condition)


class HasValue(abc.HasValue):
    __setter__: ClassVar[Optional[EvaluableSetter]]
    __getter__: ClassVar[Optional[EvaluableGetter]]

    _value_setter: Optional[DynamicSetter]
    _value_getter: Optional[DynamicGetter]

    _update_local: Callable[..., None]
    _update_model: Callable[..., None]

    @classmethod
    def _init_has_value_class(cls, kwargs: dict):
        if 'BIND' in kwargs:
            getter = setter = kwargs.get(Keys.BINDER, None)

        else:
            getter = kwargs.get(Keys.GETTER, None)
            setter = kwargs.get(Keys.SETTER, None)

        if isinstance(getter, str):
            cls.__getter__ = as_evaluable_path(path=getter)

        elif getter is None:
            cls.__getter__ = None

        else:
            raise TypeError(f"{cls.__name__}.{Keys.GETTER} should be str | None")

        if isinstance(setter, str):
            cls.__setter__ = as_evaluable_path(path=setter)

        elif setter is None:
            cls.__setter__ = None

        else:
            raise TypeError(f"{cls.__name__}.{Keys.SETTER} should be str | None")

    def __init__(self, parent_data: DynamicData = None):
        observer = Observer()

        self._value_setter = None
        self._value_getter = None

        if isinstance(parent_data, DynamicData):
            if isinstance(self.__getter__, EvaluableGetter):
                self._value_getter = DynamicGetter(data=parent_data, path=self.__getter__)

                observer.on(name=f".{self.__getter__}", emitter=parent_data, function=self._update_local)
                # observer.on(name='*', emitter=parent_data, function=print)
            elif self.__getter__ is None:
                pass
            else:
                raise Exception

            if isinstance(self.__setter__, EvaluableSetter):
                self._value_setter = DynamicSetter(data=parent_data, path=self.__setter__)

    def _update_local(self, *args, **kwargs):
        assert isinstance(self.__getter__, EvaluableGetter)
        self._set_local(self._value_getter.view())

    def _update_model(self, *args, **kwargs):
        assert isinstance(self.__setter__, EvaluableSetter)
        self._value_setter.set(self._get_local())

    def _set_local(self, value):
        """Set the local value for the widget."""
        raise Exception(f"Method {self.__class__.__name__}._set_local undefined !")

    def _get_local(self):
        """Get the local value of the widget."""
        raise Exception(f"Method {self.__class__.__name__}._get_local undefined !")


class HasStyleAndData(HasStyle, HasData, tk.Misc, abc.HasStyleAndData):
    @classmethod
    def _init_has_style_and_data_class(cls, kwargs: dict):
        cls._init_has_style_class(kwargs)
        cls._init_has_data_class(kwargs)

    def __init__(self, data: dict = None, parent_data: DynamicData = None,
                 style: dict = None, parent_style: DynamicStyle = None):
        HasData.__init__(self, data=data, parent_data=parent_data)
        HasStyle.__init__(self, style=style, parent_style=parent_style)

        self._register_style_events()

    def _register_style_events(self) -> None:
        """Make sure that style local evaluable properties rely on data."""
        for key, value in self.style.items():
            if isinstance(value, Evaluable):
                self.style.on(name='*', emitter=self.data, function=self.update_style)

    def update_style(self, _: Event = None) -> None:
        style = self.render_style()
        self.config(**style)

    def render_style(self) -> dict:
        style = {}
        data_view = self.data.view()
        style_view = self.style.view()
        valid_keys = self.keys()

        for key, value in style_view.items():
            if key in valid_keys:
                value = evaluate(value, data_view)
                value = view(value)
                style[key] = value

        _check_style_render_integrity(style)
        return style
