
# src/treexx/output/json.py

import json
from collections.abc import Iterable

from treexx.core.traversal.models import FileEntry
from treexx.output.base import OutputFormatter


class JsonFormatter(OutputFormatter):
    def render(self, entries: Iterable[FileEntry]) -> str:
        data = [
            {
                "name": file_entry.name,
                "path": file_entry.path.as_posix(),
                "relative_path": file_entry.relative_path.as_posix(),
                "type": file_entry.kind.value,
            }
            for file_entry in entries
        ]

        return json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        )
