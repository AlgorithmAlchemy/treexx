# src/treexx/core/traversal/models.py

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class EntryType(str, Enum):
    FILE = "file"
    DIRECTORY = "directory"
    SYMLINK = "symlink"


@dataclass(frozen=True, slots=True)
class FileEntry:
    path: Path
    relative_path: Path
    kind: EntryType

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def is_file(self) -> bool:
        return self.kind is EntryType.FILE

    @property
    def is_dir(self) -> bool:
        return self.kind is EntryType.DIRECTORY

    @property
    def is_symlink(self) -> bool:
        return self.kind is EntryType.SYMLINK
