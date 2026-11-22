
# src/treexx/core/traversal/walker.py

import os
from collections.abc import Iterator
from pathlib import Path

from treexx.core.filtering.engine import FilterEngine
from treexx.core.traversal.models import EntryType, FileEntry


class FileWalker:
    def __init__(
        self,
        root: Path,
        respect_gitignore: bool = True,
        show_hidden: bool = False,
    ) -> None:
        self.root = Path(os.path.abspath(root))
        self.filter_engine = FilterEngine(
            root=self.root,
            respect_gitignore=respect_gitignore,
            show_hidden=show_hidden,
        )

    def walk(self) -> Iterator[FileEntry]:
        if not self.root.is_dir():
            return

        yield from self._walk(self.root)

    def _walk(self, directory: Path) -> Iterator[FileEntry]:
        try:
            with os.scandir(directory) as entries:
                sorted_entries = sorted(
                    entries,
                    key=lambda entry: (
                        entry.name.casefold(),
                        entry.name,
                    ),
                )
        except OSError:
            return

        for entry in sorted_entries:
            path = Path(entry.path)
            relative_path = path.relative_to(self.root)

            try:
                is_symlink = entry.is_symlink()

                if is_symlink:
                    is_dir = False
                else:
                    is_dir = entry.is_dir(
                        follow_symlinks=False,
                    )
            except OSError:
                continue

            if not self.filter_engine.should_include(
                path,
                is_dir=is_dir,
            ):
                continue

            if is_symlink:
                yield FileEntry(
                    path=path,
                    relative_path=relative_path,
                    kind=EntryType.SYMLINK,
                )
                continue

            if is_dir:
                yield FileEntry(
                    path=path,
                    relative_path=relative_path,
                    kind=EntryType.DIRECTORY,
                )

                yield from self._walk(path)
                continue

            yield FileEntry(
                path=path,
                relative_path=relative_path,
                kind=EntryType.FILE,
            )
