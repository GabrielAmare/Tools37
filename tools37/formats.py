from __future__ import annotations

import re
import typing
import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime

# from typing import Optional, Callable, TypeVar, Generic, Type, Tuple

E = t.TypeVar('E')
F = t.TypeVar('F')

__all__ = [
    'Parser',
    'Identity',
    # abstracts
    'Format',
    'TypedFormat',
    'Atom',
    'Iter',
    # utils
    'ParsingError',
    # simples
    'Boolean',
    'Integer',
    'Decimal',
    'String',
    'Date',
    'Datetime',
    # nested
    'List',
    'Dict'
]


########################################################################################################################
# UTILS
########################################################################################################################

class Parser(t.Generic[F], ABC):
    @abstractmethod
    def __call__(self) -> F:
        """"""


class Identity(t.Generic[E], Parser[E]):
    def __init__(self, data: E):
        self.data: E = data

    def __call__(self) -> E:
        return self.data


class ParserFromValue(t.Generic[E], Parser[E]):
    def __init__(self, value: E):
        self.value: E = value

    def __call__(self) -> E:
        return self.value


class ParserFromFunction(t.Generic[E], Parser[E]):
    def __init__(self, function: t.Callable[[], E]):
        self.function: t.Callable[[], E] = function

    def __call__(self):
        return self.function()


class DataParser(t.Generic[E, F], Parser[F]):
    def __init__(self, function: t.Callable[[E], F], data: F):
        self.function: t.Callable[[E], F] = function
        self.data: F = data

    def __call__(self) -> F:
        return self.function(self.data)

    @classmethod
    def wrapper(cls, function: t.Callable[[E], F]) -> t.Callable[[E], Parser[F]]:
        def wrapped(data: E) -> Parser[F]:
            return DataParser(function, data)

        return wrapped


########################################################################################################################
# ERRORS
########################################################################################################################

@dataclass
class ParsingError(Exception):
    path: str
    data: object
    output_type: type
    reason: str

    def __str__(self):
        return f"{self.path!s}: {self.data.__class__.__name__!s} = {self.data!r} --> {self.reason!r}"

    def __call__(self) -> t.NoReturn:
        raise self


########################################################################################################################
# DATA PARSERS
########################################################################################################################

@DataParser.wrapper
def date_to_string(value: date) -> str:
    return value.isoformat()


@DataParser.wrapper
def datetime_to_string(value: datetime) -> str:
    return value.isoformat()


@DataParser.wrapper
def string_to_date(value: str) -> date:
    return date.fromisoformat(value)


@DataParser.wrapper
def string_to_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


@DataParser.wrapper
def to_int(value: t.Union[bool, float, str]) -> int:
    return int(value)


@DataParser.wrapper
def to_bool(value: int) -> bool:
    return bool(value)


@DataParser.wrapper
def to_str(value: object) -> str:
    return str(value)


@DataParser.wrapper
def to_float(value: t.Union[bool, int, str]) -> float:
    return float(value)


########################################################################################################################
# ABSTRACT FORMATS
########################################################################################################################


class Format(ABC):
    @abstractmethod
    def get_parser(self, data: object, path: str = '') -> t.Union[Parser[E], ParsingError]:
        """"""

    def parse(self, data, path: str = ''):
        parser = self.get_parser(data, path)

        if isinstance(parser, ParsingError):
            raise parser

        return parser()


class TypedFormat(t.Generic[E], Format, ABC):
    datatype: t.Type[E]


class Atom(t.Generic[E], TypedFormat[E], ABC):
    def __init__(self,
                 default: E = None,
                 default_factory: t.Callable[[], E] = None,
                 optional: bool = False,
                 ):
        """

        :param default: default value (if specified)
        :param default_factory: default factory (if specified)
        :param optional: if True, None value is allowed
        """
        assert default is None or default_factory is None, 'cannot specify both `default` and `default_factory`'
        self.default: t.Optional[E] = default
        self.default_factory: t.Optional[t.Callable[[], E]] = default_factory
        self.optional: bool = optional

    def __repr__(self) -> str:
        contents = []

        if self.default is not None:
            contents.append(f"default={self.default!r}")

        if self.default_factory is not None:
            contents.append(f"default_factory={self.default_factory.__name__!s}")

        if self.optional:
            contents.append("optional=True")

        return f"{self.__class__.__name__}({', '.join(contents)})"

    def get_parser(self, data: object, path: str = '') -> t.Union[Parser[E], ParsingError]:
        if data is None:
            if self.optional:
                return Identity(data)

            if self.default is not None:
                return ParserFromValue(self.default)

            if self.default_factory is not None:
                return ParserFromFunction(self.default_factory)

            return ParsingError(path, data, self.datatype, "wrong data type.")

        if type(data) is self.datatype:
            return Identity(data)

        return ParsingError(path, data, self.datatype, "wrong data type.")


class Iter(t.Generic[E], TypedFormat[E], ABC):
    def __init__(self, items_format: Format):
        self.items_format: Format = items_format

    def __repr__(self):
        return f"{self.__class__.__name__}({self.items_format!r})"


########################################################################################################################
# SIMPLE FORMATS
########################################################################################################################


class Integer(Atom[int]):
    datatype = int

    def get_parser(self, data: object, path: str = '') -> t.Union[Parser[int], ParsingError]:
        parser = super().get_parser(data, path)

        if not isinstance(parser, ParsingError):
            return parser

        if isinstance(data, float):
            if data % 1 == 0:
                return to_int(data)

            return ParsingError(path, data, int, "shouldn't have a decimal part.")

        if isinstance(data, bool):
            return to_int(data)

        if isinstance(data, str):
            if data.isnumeric():
                return to_int(data)

            return ParsingError(path, data, int, "should be composed only of digits.")

        return parser


class String(Atom[str]):
    datatype = str

    def get_parser(self, data, path: str = '') -> t.Union[Parser[str], ParsingError]:
        parser = super().get_parser(data, path)

        if not isinstance(parser, ParsingError):
            return parser

        if isinstance(data, bool):
            return to_str(data)

        if isinstance(data, int):
            return to_str(data)

        if isinstance(data, float):
            return to_str(data)

        if isinstance(data, date):
            return date_to_string(data)

        if isinstance(data, datetime):
            return datetime_to_string(data)

        return parser


class Decimal(Atom[float]):
    datatype = float

    def get_parser(self, data, path: str = '') -> t.Union[Parser[float], ParsingError]:
        parser = super().get_parser(data, path)

        if not isinstance(parser, ParsingError):
            return parser

        if isinstance(data, int):
            return to_float(data)

        if isinstance(data, bool):
            return to_float(data)

        if isinstance(data, str):
            if data == 'inf':
                return to_float(data)

            if data == '-inf':
                return to_float(data)

            if data == 'nan':
                return to_float(data)

            if re.match(r'^(\d+|\d+\.\d*|\.\d+)$', data):
                return to_float(data)

            return ParsingError(path, data, float, "should be 'inf', '-inf', 'nan', or any valid decimal number.")

        return parser


class Boolean(Atom[bool]):
    datatype = bool

    def get_parser(self, data, path: str = '') -> t.Union[Parser[bool], ParsingError]:
        parser = super().get_parser(data, path)

        if not isinstance(parser, ParsingError):
            return parser

        if isinstance(data, int):
            if data == 0:
                return ParserFromValue(False)

            if data == 1:
                return ParserFromValue(True)

            return ParsingError(path, data, bool, "should be `0` or `1`.")

        if isinstance(data, float):
            if data == 0.0:
                return ParserFromValue(False)

            if data == 1.0:
                return ParserFromValue(True)

            return ParsingError(path, data, bool, "should be `0.0` or `1.0`.")

        if isinstance(data, str):
            if data == "False":
                return ParserFromValue(False)

            if data == "True":
                return ParserFromValue(True)

            return ParsingError(path, data, bool, "should be 'False' or 'True'.")

        return parser


class Date(Atom[date]):
    datatype = date

    def get_parser(self, data, path: str = '') -> t.Union[Parser[date], ParsingError]:
        parser = super().get_parser(data, path)

        if not isinstance(parser, ParsingError):
            return parser

        if isinstance(data, str):
            if re.match(r'^\d{4}-\d{2}-\d{2}$', data):
                return string_to_date(data)

            return ParsingError(path, data, date, "invalid date iso-format.")

        return parser


class Datetime(Atom[datetime]):
    datatype = datetime

    def get_parser(self, data, path: str = '') -> t.Union[Parser[datetime], ParsingError]:
        parser = super().get_parser(data, path)

        if not isinstance(parser, ParsingError):
            return parser

        if isinstance(data, str):
            if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$', data):
                return string_to_datetime(data)

            return ParsingError(path, data, self.datatype, "invalid datetime iso-format.")

        return parser


########################################################################################################################
# NESTED FORMATS
########################################################################################################################


class List(Iter[list]):
    def get_parser(self, data: object, path: str = '') -> t.Union[Parser[list], ParsingError]:
        if data is None:
            return ParserFromFunction(list)

        if isinstance(data, list):
            item_parsers = [
                self.items_format.get_parser(item, path=f"{path}[{index}]")
                for index, item in enumerate(data)
            ]

            def parser() -> list:
                return list(item_parser() for item_parser in item_parsers)

            return ParserFromFunction(parser)

        return ParsingError(path, data, self.datatype, "wrong data type.")


class Tuple(Iter[tuple]):
    def get_parser(self, data, path: str = '') -> t.Union[Parser[tuple], ParsingError]:
        if data is None:
            return ParserFromFunction(tuple)

        if isinstance(data, tuple):
            item_parsers = [
                self.items_format.get_parser(item, path=f"{path}[{index}]")
                for index, item in enumerate(data)
            ]

            def parser() -> tuple:
                return tuple(item_parser() for item_parser in item_parsers)

            return ParserFromFunction(parser)

        return ParsingError(path, data, self.datatype, "wrong data type.")


class Dict(TypedFormat[dict]):
    datatype = dict

    def __init__(self,
                 __strict__: bool = False,
                 **fields: Format,
                 ):
        self.__strict__: bool = __strict__
        self.fields: typing.Dict[str, Format] = fields

    def __repr__(self) -> str:
        contents = []
        for key, field in self.fields.items():
            contents.append(f"{key!s}={field!r}")
        if self.__strict__:
            contents.append("__strict__=True")
        return f"{self.__class__.__name__}({', '.join(contents)})"

    def get_parser(self, data, path: str = '') -> t.Union[Parser[dict], ParsingError]:
        if data is None:
            data = {}

        if type(data) is self.datatype:
            if self.__strict__:
                invalid_keys = []
                for key in data.keys():
                    if key not in self.fields:
                        invalid_keys.append(key)

                if invalid_keys:
                    # TODO : make it return a parsing error
                    return ParsingError(path, data, self.datatype, f"the keys : {invalid_keys!r} are not allowed !")

            field_parsers = {
                key: field.get_parser(data=data.get(key), path=f"{path}[{key!r}]")
                for key, field in self.fields.items()
            }
            if any(isinstance(field_parser, ParsingError) for field_parser in field_parsers.values()):
                return ParsingError(path, data, self.datatype,
                                    "\n\t".join(
                                        f"  - {key!s} -> {field_parser}"
                                        for key, field_parser in field_parsers.items()
                                        if isinstance(field_parser, ParsingError)
                                    )
                                    )

            def parser():
                return {key: field_parser() for key, field_parser in field_parsers.items()}

            return ParserFromFunction(parser)

        return ParsingError(path, data, self.datatype, "wrong data type.")

    def omit(self, *keys_to_omit, __strict__: bool = None) -> Dict:
        """Return a new format where some keys are omitted."""
        return Dict(
            __strict__=self.__strict__ if __strict__ is None else __strict__,
            **{
                key: field
                for key, field in self.fields.items()
                if key not in keys_to_omit
            }
        )

    def keep(self, *keys_to_keep, __strict__: bool = None) -> Dict:
        """Return a new format where only some keys are keeped."""
        return Dict(
            __strict__=self.__strict__ if __strict__ is None else __strict__,
            **{
                key: field
                for key, field in self.fields.items()
                if key in keys_to_keep
            }
        )


########################################################################################################################
# SPECIAL FORMATS
########################################################################################################################


class Union(Format):
    def __init__(self, *options: Format, unique: bool = False):
        self.options: t.Tuple[Format, ...] = options
        self.unique: bool = unique

    def get_parser(self, data, path: str = '') -> t.Union[Parser[object], ParsingError]:
        errors = []
        parsers = []
        for option in self.options:
            option_parser = option.get_parser(data, path)

            if isinstance(option_parser, Identity):
                return option_parser

            elif isinstance(option_parser, ParsingError):
                errors.append(option_parser)

            else:
                parsers.append(option_parser)

        if len(parsers) > 1 and self.unique:
            return ParsingError(path, data, object,
                                f"multiple parsers {', '.join(map(repr, (parser.__name__ for parser in parsers)))}.")
        if len(parsers) > 0:
            return parsers[0]

        if len(errors) == 1:
            return errors[0]

        return ParsingError(path, data, object, "\n\t| ".join(
            str(option_parser)
            for option_parser in parsers
        ))
