
# src/treexx/application/dto/query.py

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TreeQuery:
    root: Path
    show_all: bool = False
    show_hidden: bool = False
    max_depth: int | None = None
    respect_gitignore: bool = True


@dataclass(frozen=True, slots=True)
class ListQuery:
    root: Path
    show_all: bool = False
    show_hidden: bool = False
    respect_gitignore: bool = True


@dataclass(frozen=True, slots=True)
class FindQuery:
    root: Path
    pattern: str
    show_hidden: bool = False
    respect_gitignore: bool = True


@dataclass(frozen=True, slots=True)
class DiskUsageQuery:
    root: Path
    show_hidden: bool = False
    respect_gitignore: bool = True
