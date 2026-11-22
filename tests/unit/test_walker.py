
# tests/unit/test_walker.py

import os
from pathlib import Path

import pytest

from treexx.core.traversal.models import EntryType
from treexx.core.traversal.walker import FileWalker


def test_walk_returns_files_and_directories_in_sorted_order(
    tmp_path: Path,
) -> None:
    (tmp_path / "b.txt").write_text("B", encoding="utf-8")
    (tmp_path / "a.txt").write_text("A", encoding="utf-8")

    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.txt").write_text("C", encoding="utf-8")

    entries = list(
        FileWalker(
            root=tmp_path,
            respect_gitignore=False,
        ).walk()
    )

    relative_paths = [
        entry.relative_path.as_posix()
        for entry in entries
    ]

    assert relative_paths == [
        "a.txt",
        "b.txt",
        "nested",
        "nested/c.txt",
    ]


def test_walk_returns_correct_entry_types(
    tmp_path: Path,
) -> None:
    (tmp_path / "file.txt").write_text(
        "content",
        encoding="utf-8",
    )
    (tmp_path / "directory").mkdir()

    entries = list(
        FileWalker(
            root=tmp_path,
            respect_gitignore=False,
        ).walk()
    )

    entry_types = {
        entry.name: entry.kind
        for entry in entries
    }

    assert entry_types == {
        "directory": EntryType.DIRECTORY,
        "file.txt": EntryType.FILE,
    }


def test_walk_does_not_follow_symbolic_links(
    tmp_path: Path,
) -> None:
    root = tmp_path / "root"
    root.mkdir()

    external_directory = tmp_path / "external"
    external_directory.mkdir()
    (external_directory / "secret.txt").write_text(
        "content",
        encoding="utf-8",
    )

    link_path = root / "linked"

    try:
        link_path.symlink_to(
            external_directory,
            target_is_directory=True,
        )
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"Symbolic links are unavailable: {exc}")

    entries = list(
        FileWalker(
            root=root,
            respect_gitignore=False,
        ).walk()
    )

    relative_paths = {
        entry.relative_path.as_posix()
        for entry in entries
    }

    assert relative_paths == {"linked"}


def test_walk_returns_empty_result_for_empty_directory(
    tmp_path: Path,
) -> None:
    entries = list(
        FileWalker(
            root=tmp_path,
            respect_gitignore=False,
        ).walk()
    )

    assert entries == []


@pytest.mark.skipif(
    os.name == "nt",
    reason="Windows uses filesystem attributes for hidden entries",
)
def test_walk_excludes_hidden_entries_by_default(
    tmp_path: Path,
) -> None:
    (tmp_path / ".hidden.txt").write_text(
        "hidden",
        encoding="utf-8",
    )

    hidden_directory = tmp_path / ".hidden"
    hidden_directory.mkdir()
    (hidden_directory / "secret.txt").write_text(
        "secret",
        encoding="utf-8",
    )

    (tmp_path / "visible.txt").write_text(
        "visible",
        encoding="utf-8",
    )

    entries = list(
        FileWalker(
            root=tmp_path,
            respect_gitignore=False,
        ).walk()
    )

    relative_paths = {
        entry.relative_path.as_posix()
        for entry in entries
    }

    assert relative_paths == {"visible.txt"}


@pytest.mark.skipif(
    os.name == "nt",
    reason="Windows uses filesystem attributes for hidden entries",
)
def test_walk_includes_hidden_entries_when_enabled(
    tmp_path: Path,
) -> None:
    (tmp_path / ".hidden.txt").write_text(
        "hidden",
        encoding="utf-8",
    )

    hidden_directory = tmp_path / ".hidden"
    hidden_directory.mkdir()
    (hidden_directory / "secret.txt").write_text(
        "secret",
        encoding="utf-8",
    )

    entries = list(
        FileWalker(
            root=tmp_path,
            respect_gitignore=False,
            show_hidden=True,
        ).walk()
    )

    relative_paths = {
        entry.relative_path.as_posix()
        for entry in entries
    }

    assert relative_paths == {
        ".hidden",
        ".hidden/secret.txt",
        ".hidden.txt",
    }
