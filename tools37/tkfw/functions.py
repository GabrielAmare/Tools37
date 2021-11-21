from typing import Union, Callable, TypeVar, Type, Optional

__all__ = [
    'indent',
    'print_indent',
    'print_method',
    'update_dict_from_dict_or_factory',
    'init_dict_from_dicts_and_factories',
    'init_from_factory'
]


def indent(s: str, prefix: str = '  ') -> str:
    return '\n'.join(prefix + line for line in s.split('\n'))


_INDENT = 0


def repr_method(cls, method, self, args, kwargs):
    head = repr(self) if self else cls.__name__

    try:
        props = []

        for arg in args:
            props.append(f"{arg!r}")

        for key, value in kwargs.items():
            props.append(f"{key!s}={value!r}")

        return f"{head}.{method.__name__}({', '.join(props)})"

    except Exception:
        return f"{head}.{method.__name__}(...)"


def print_indent(message):
    print(indent(message, prefix=_INDENT * '\t'))


def print_method(method):
    def wrapped(self, *args, **kwargs):
        global _INDENT

        self_ = None if method.__name__ == '__init__' else self

        print_indent(repr_method(self.__class__, method, self_, args, kwargs))

        _INDENT += 1
        result = method(self, *args, **kwargs)
        _INDENT -= 1

        return result

    return wrapped


def update_dict_from_dict_or_factory(dict_to_update: dict, using: Union[dict, Callable[[], dict]]) -> None:
    if isinstance(using, dict):
        dict_to_update.update(using)

    elif hasattr(using, '__call__'):
        dict_to_update.update(using())

    else:
        raise TypeError(using)


def init_dict_from_dicts_and_factories(*args: Union[None, dict, Callable[[], dict]]) -> dict:
    result = {}

    for arg in args:
        if arg is not None:
            update_dict_from_dict_or_factory(result, arg)

    return result


F = TypeVar('F')


def init_from_factory(factory: Type[F],
                      parent: Optional[F],
                      dict_local: Optional[dict],
                      dict_factory: Optional[Callable[[], dict]]
                      ) -> F:
    local = init_dict_from_dicts_and_factories(dict_local, dict_factory)

    if not local and isinstance(parent, factory):
        return parent

    else:
        return factory(local, parent)
