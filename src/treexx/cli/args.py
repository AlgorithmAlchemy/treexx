
# src/treexx/cli/args.py

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class CLIArguments:
    command: str
    root: Path
    pattern: str | None = None
    show_files: bool = False
    show_hidden: bool = False
    respect_gitignore: bool = True
    output_format: str = "text"


def _add_common_arguments(
    parser: argparse.ArgumentParser,
) -> None:
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Root directory",
    )
    parser.add_argument(
        "--hidden",
        action="store_true",
        help="Include hidden and system entries",
    )
    parser.add_argument(
        "--no-ignore",
        action="store_true",
        help="Do not respect .gitignore rules",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="treex",
        description="Filesystem traversal toolkit",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    tree_parser = subparsers.add_parser(
        "tree",
        help="Display directory tree",
    )
    _add_common_arguments(tree_parser)
    tree_parser.add_argument(
        "-f",
        "--files",
        action="store_true",
        help="Include files in the tree",
    )

    ls_parser = subparsers.add_parser(
        "ls",
        help="List directory contents",
    )
    _add_common_arguments(ls_parser)

    find_parser = subparsers.add_parser(
        "find",
        help="Find files and directories by name",
    )
    find_parser.add_argument("pattern")
    _add_common_arguments(find_parser)

    du_parser = subparsers.add_parser(
        "du",
        help="Calculate directory size",
    )
    _add_common_arguments(du_parser)

    return parser


def parse_args(
    argv: Sequence[str] | None = None,
) -> CLIArguments:
    arguments = list(sys.argv[1:] if argv is None else argv)

    if not arguments:
        arguments = ["tree"]
    elif arguments[0] not in {"tree", "ls", "find", "du"}:
        arguments.insert(0, "tree")

    arguments = [
        "--files" if argument == "/f" else argument
        for argument in arguments
    ]

    namespace = build_parser().parse_args(arguments)

    return CLIArguments(
        command=namespace.command,
        root=namespace.root,
        pattern=getattr(namespace, "pattern", None),
        show_files=getattr(namespace, "files", False),
        show_hidden=namespace.hidden,
        respect_gitignore=not namespace.no_ignore,
        output_format=(
            "json" if namespace.json else "text"
        ),
    )
