
# src/treexx/output/base.py

from abc import ABC, abstractmethod
from collections.abc import Iterable

from treexx.core.traversal.models import FileEntry


class OutputFormatter(ABC):
    @abstractmethod
    def render(self, entries: Iterable[FileEntry]) -> str:
        pass
