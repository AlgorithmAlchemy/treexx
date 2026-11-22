
# src/treexx/output/ls.py

from collections.abc import Iterable

from treexx.core.traversal.models import EntryType, FileEntry
from treexx.output.base import OutputFormatter


class LsFormatter(OutputFormatter):
    def render(self, entries: Iterable[FileEntry]) -> str:
        lines: list[str] = []

        for file_entry in entries:
            name = file_entry.name

            if file_entry.kind is EntryType.DIRECTORY:
                name += "/"
            elif file_entry.kind is EntryType.SYMLINK:
                name += " @"

            lines.append(name)

        return "\n".join(lines)
