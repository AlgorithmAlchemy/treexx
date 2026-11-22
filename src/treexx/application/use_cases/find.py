# src/treexx/application/use_cases/find.py

from collections.abc import Iterator
from fnmatch import fnmatchcase

from treexx.application.dto.query import FindQuery
from treexx.core.traversal.models import FileEntry
from treexx.core.traversal.walker import FileWalker


class FindUseCase:
    @staticmethod
    def execute(query: FindQuery) -> Iterator[FileEntry]:
        walker = FileWalker(
            root=query.root,
            respect_gitignore=query.respect_gitignore,
            show_hidden=query.show_hidden,
        )

        pattern = query.pattern.casefold()

        for file_entry in walker.walk():
            if fnmatchcase(file_entry.name.casefold(), pattern):
                yield file_entry
