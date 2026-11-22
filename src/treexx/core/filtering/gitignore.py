
# src/treexx/core/filtering/gitignore.py

import os
from pathlib import Path

from pathspec import PathSpec


class GitIgnore:
    def __init__(self, root: Path) -> None:
        self.root = Path(os.path.abspath(root))
        self._cache: dict[Path, PathSpec | None] = {}

    def is_ignored(self, path: Path, is_dir: bool = False) -> bool:
        path = self._normalize_path(path)

        if path == self.root:
            return False

        relative_path = path.relative_to(self.root)

        for parent in relative_path.parents:
            if parent == Path("."):
                continue

            parent_path = self.root / parent

            if self._matches(parent_path, is_dir=True):
                return True

        return self._matches(path, is_dir=is_dir)

    def _matches(self, path: Path, is_dir: bool) -> bool:
        ignored = False

        for directory in self._get_rule_directories(path, is_dir):
            spec = self._load_spec(directory)

            if spec is None:
                continue

            relative_path = path.relative_to(directory).as_posix()

            if is_dir and directory == path:
                relative_path = "."

            elif is_dir:
                relative_path += "/"

            result = spec.check_file(relative_path)

            if result.include is not None:
                ignored = result.include

        return ignored

    def _get_rule_directories(
        self,
        path: Path,
        is_dir: bool,
    ) -> list[Path]:
        directories = [self.root]

        relative_path = path.relative_to(self.root)
        parents = list(relative_path.parents)

        for parent in reversed(parents):
            if parent == Path("."):
                continue

            directories.append(self.root / parent)

        if is_dir:
            directories.append(path)

        return directories

    def _load_spec(self, directory: Path) -> PathSpec | None:
        if directory in self._cache:
            return self._cache[directory]

        ignore_file = directory / ".gitignore"

        if not ignore_file.is_file():
            self._cache[directory] = None
            return None

        try:
            content = ignore_file.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            self._cache[directory] = None
            return None

        spec = PathSpec.from_lines(
            "gitwildmatch",
            content.splitlines(),
        )

        self._cache[directory] = spec
        return spec

    def _normalize_path(self, path: Path) -> Path:
        if not path.is_absolute():
            path = self.root / path

        normalized = Path(os.path.abspath(path))

        try:
            normalized.relative_to(self.root)
        except ValueError as exc:
            raise ValueError(
                f"Path is outside the root directory: {path}"
            ) from exc

        return normalized
