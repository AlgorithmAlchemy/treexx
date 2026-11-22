# src/treexx/application/use_cases/du.py

from treexx.application.dto.query import DiskUsageQuery
from treexx.core.traversal.models import EntryType
from treexx.core.traversal.walker import FileWalker


class DiskUsageUseCase:
    @staticmethod
    def execute(query: DiskUsageQuery) -> int:
        walker = FileWalker(
            root=query.root,
            respect_gitignore=query.respect_gitignore,
            show_hidden=query.show_hidden,
        )

        total_size = 0

        for file_entry in walker.walk():
            if file_entry.kind is not EntryType.FILE:
                continue

            try:
                total_size += file_entry.path.stat().st_size
            except OSError:
                continue

        return total_size
