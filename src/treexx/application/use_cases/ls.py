# src/treexx/application/use_cases/ls.py

from collections.abc import Iterator

from treexx.application.dto.query import ListQuery
from treexx.core.traversal.models import FileEntry
from treexx.core.traversal.walker import FileWalker


class LsUseCase:
    @staticmethod
    def execute(query: ListQuery) -> Iterator[FileEntry]:
        walker = FileWalker(
            root=query.root,
            respect_gitignore=query.respect_gitignore,
            show_hidden=query.show_hidden,
        )

        for file_entry in walker.walk():
            if len(file_entry.relative_path.parts) == 1:
                yield file_entry
