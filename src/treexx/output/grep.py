
# src/treexx/output/grep.py

from collections.abc import Iterable

from treexx.core.traversal.models import FileEntry
from treexx.output.base import OutputFormatter


class GrepFormatter(OutputFormatter):
    def render(self, entries: Iterable[FileEntry]) -> str:
        return "\n".join(
            file_entry.relative_path.as_posix()
            for file_entry in entries
        )
