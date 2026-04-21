# path/to/src/treexx/core/traversal/walker.py

import os
from collections.abc import Iterator
from pathlib import Path
from typing import Callable, Optional


class FileWalker:
    def __init__(
        self,
        root: str,
        filter_fn: Optional[Callable[[Path], bool]] = None,
    ):
        self.root = Path(root)
        self.filter_fn = filter_fn or (lambda _: True)

    def walk(self) -> Iterator[Path]:
        yield from self._walk(self.root)

    def _walk(self, path: Path) -> Iterator[Path]:
        try:
            with os.scandir(path) as it:
                entries = sorted(it, key=lambda e: e.name)

                for entry in entries:
                    entry_path = Path(entry.path)

                    is_dir = entry.is_dir(follow_symlinks=False)

                    # IMPORTANT: allow filtering directories too
                    if not self.filter_fn(entry_path):
                        continue

                    if is_dir:
                        yield from self._walk(entry_path)
                    else:
                        yield entry_path

        except (PermissionError, FileNotFoundError):
            return