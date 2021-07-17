import os
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional, Generic

E = TypeVar('E')


class FileView(Generic[E], ABC):
    def __init__(self, file_path: str, factory: Type[E]):
        """

        :param file_path: The path of the file.
        :param factory: The factory to build resource from file data.
        """
        self.file_path: str = file_path
        self.factory: Type[E] = factory
        self.resource: Optional[E] = None
        self.load()

    def exists(self) -> bool:
        """Return True if the file exists."""
        return os.path.exists(self.file_path)

    @abstractmethod
    def load(self) -> None:
        """Load the file as resource."""

    @abstractmethod
    def save(self) -> None:
        """Save the resource as file."""
