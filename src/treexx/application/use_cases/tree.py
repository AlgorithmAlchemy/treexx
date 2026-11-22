# src/treexx/application/use_cases/tree.py

from collections.abc import Iterator

from treexx.application.dto.query import TreeQuery
from treexx.core.traversal.models import FileEntry
from treexx.core.traversal.walker import FileWalker


class TreeUseCase:
    @staticmethod
    def execute(query: TreeQuery) -> Iterator[FileEntry]:
        walker = FileWalker(
            root=query.root,
            respect_gitignore=query.respect_gitignore,
            show_hidden=query.show_hidden,
        )

        for file_entry in walker.walk():
            if (
                query.max_depth is not None
                and len(file_entry.relative_path.parts) > query.max_depth
            ):
                continue

            yield file_entry
