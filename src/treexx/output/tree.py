
# src/treexx/output/tree.py

from collections.abc import Iterable
from pathlib import PurePosixPath

from treexx.core.traversal.models import EntryType, FileEntry
from treexx.output.base import OutputFormatter


class TreeFormatter(OutputFormatter):
    def render(self, entries: Iterable[FileEntry]) -> str:
        entry_list = list(entries)
        children: dict[PurePosixPath, list[FileEntry]] = {}

        for file_entry in entry_list:
            parent = PurePosixPath(*file_entry.relative_path.parts[:-1])
            children.setdefault(parent, []).append(file_entry)

        lines: list[str] = []

        def render_directory(
            parent: PurePosixPath,
            prefix: str,
        ) -> None:
            directory_entries = children.get(parent, [])

            for index, file_entry in enumerate(directory_entries):
                is_last = index == len(directory_entries) - 1
                connector = "└── " if is_last else "├── "
                extension = "    " if is_last else "│   "

                name = file_entry.name

                if file_entry.kind is EntryType.DIRECTORY:
                    name += "/"
                elif file_entry.kind is EntryType.SYMLINK:
                    name += " @"

                lines.append(f"{prefix}{connector}{name}")

                if file_entry.kind is EntryType.DIRECTORY:
                    child_path = PurePosixPath(
                        *file_entry.relative_path.parts
                    )
                    render_directory(child_path, prefix + extension)

        render_directory(PurePosixPath(), "")
        return "\n".join(lines)
