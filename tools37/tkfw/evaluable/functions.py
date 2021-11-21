import re
from typing import Union, List, Any

from .abc import *
from .base import *

__all__ = [
    'as_evaluable_path',
    'as_evaluable_text',
    'evaluate',
    'as_evaluable_expression'
]

_PATTERN_REGEX = re.compile(r'{{[^{}]*?}}')


def _string_as_evaluable_binder(string: str) -> EvaluableBinder:
    if string.isnumeric():
        return EvaluableListItem(index=int(string))

    elif string.isidentifier():
        return EvaluableDictItem(key=string)

    else:
        raise ValueError(f"Invalid key {string!r}. Should be numeric | identifier.")


def as_evaluable_path(path: str) -> EvaluablePath:
    if not path:
        raise ValueError(f"Invalid path {path!r} with dynamic binder model.")

    return EvaluablePath(steps=[
        _string_as_evaluable_binder(arg)
        for arg in path.split('.')
    ])


def as_evaluable_text(string: str) -> Union[str, EvaluableText]:
    start: int = 0
    string_to_format: str = ''
    values: List[EvaluableBinder] = []

    matches = _PATTERN_REGEX.finditer(string)

    for index, match in enumerate(matches):
        string_to_format += string[start: match.start()] + "{" + str(index) + "}"

        value = as_evaluable_path(path=match.group()[2:-2].strip())

        values.append(value)

        start = match.end()

    string_to_format += string[start:]

    if not values:
        return string

    return EvaluableText(expression=string_to_format, values=values)


def evaluate(value: Any, data: Any) -> Any:
    if isinstance(value, Evaluable):
        return value.evaluate(data)

    else:
        return value


_STRING_REGEX = re.compile(r'^(\'[^\']*?\'|\"[^\"]*?\")$')


def as_evaluable_expression(expr: str) -> EvaluableExpression:
    expr = expr.strip()

    if expr.startswith('not '):
        right_path = expr[len('not '):]
        return EvaluableNot(
            right=as_evaluable_expression(right_path)
        )

    elif ' and ' in expr:
        left_path, right_path = expr.split(' and ', 1)
        return EvaluableAnd(
            left=as_evaluable_expression(left_path),
            right=as_evaluable_expression(right_path),
        )

    elif '==' in expr:
        left_path, right_path = expr.split('==', 1)
        return EvaluableEq(
            left=as_evaluable_expression(left_path),
            right=as_evaluable_expression(right_path),
        )

    elif '!=' in expr:
        left_path, right_path = expr.split('!=', 1)
        return EvaluableNe(
            left=as_evaluable_expression(left_path),
            right=as_evaluable_expression(right_path),
        )

    elif _STRING_REGEX.match(expr):
        return EvaluableStr(value=expr)

    else:
        return as_evaluable_path(path=expr)
