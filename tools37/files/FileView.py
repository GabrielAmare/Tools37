from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional, Generic

from .PathView import PathView

E = TypeVar('E')


class FileView(Generic[E], PathView, ABC):
    def __init__(self, path: str, factory: Type[E]):
        """

        :param file_path: The path of the file.
        :param factory: The factory to build resource from file data.
        """
        super().__init__(path)
        self.factory: Type[E] = factory
        self.resource: Optional[E] = None

    @abstractmethod
    def load(self) -> None:
        """Load the file as resource."""

    @abstractmethod
    def save(self) -> None:
        """Save the resource as file."""
