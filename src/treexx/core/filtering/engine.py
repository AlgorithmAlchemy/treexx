
# src/treexx/core/filtering/engine.py

import os
import stat
from pathlib import Path

from treexx.core.filtering.gitignore import GitIgnore


class FilterEngine:
    def __init__(
        self,
        root: Path,
        respect_gitignore: bool = True,
        show_hidden: bool = False,
    ) -> None:
        self._gitignore = (
            GitIgnore(root) if respect_gitignore else None
        )
        self._show_hidden = show_hidden

    def should_include(
        self,
        path: Path,
        is_dir: bool = False,
    ) -> bool:
        if not self._show_hidden and self._is_hidden(path):
            return False

        if self._gitignore is None:
            return True

        return not self._gitignore.is_ignored(
            path,
            is_dir=is_dir,
        )

    @staticmethod
    def _is_hidden(path: Path) -> bool:
        if os.name != "nt":
            return path.name.startswith(".")

        try:
            attributes = path.stat(
                follow_symlinks=False,
            ).st_file_attributes
        except OSError:
            return False

        if attributes is None:
            return False

        hidden = getattr(stat, "FILE_ATTRIBUTE_HIDDEN", 0x02)
        system = getattr(stat, "FILE_ATTRIBUTE_SYSTEM", 0x04)

        return bool(attributes & (hidden | system))
