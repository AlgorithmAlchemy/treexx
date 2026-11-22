
# src/treexx/cli/router.py

from treexx.application.dto.query import (
    DiskUsageQuery,
    FindQuery,
    ListQuery,
    TreeQuery,
)
from treexx.application.use_cases.du import DiskUsageUseCase
from treexx.application.use_cases.find import FindUseCase
from treexx.application.use_cases.ls import LsUseCase
from treexx.application.use_cases.tree import TreeUseCase
from treexx.cli.args import CLIArguments
from treexx.output.grep import GrepFormatter
from treexx.output.json import JsonFormatter
from treexx.output.ls import LsFormatter
from treexx.output.tree import TreeFormatter


def route(arguments: CLIArguments) -> str:
    if arguments.command == "tree":
        query = TreeQuery(
            root=arguments.root,
            show_all=arguments.show_files,
            show_hidden=arguments.show_hidden,
            respect_gitignore=arguments.respect_gitignore,
        )
        entries = TreeUseCase().execute(query)

        formatter = (
            JsonFormatter()
            if arguments.output_format == "json"
            else TreeFormatter()
        )

        return formatter.render(entries)

    if arguments.command == "ls":
        query = ListQuery(
            root=arguments.root,
            show_hidden=arguments.show_hidden,
            respect_gitignore=arguments.respect_gitignore,
        )
        entries = LsUseCase().execute(query)

        formatter = (
            JsonFormatter()
            if arguments.output_format == "json"
            else LsFormatter()
        )

        return formatter.render(entries)

    if arguments.command == "find":
        if arguments.pattern is None:
            raise ValueError("Find command requires a pattern")

        query = FindQuery(
            root=arguments.root,
            pattern=arguments.pattern,
            show_hidden=arguments.show_hidden,
            respect_gitignore=arguments.respect_gitignore,
        )
        entries = FindUseCase().execute(query)

        formatter = (
            JsonFormatter()
            if arguments.output_format == "json"
            else GrepFormatter()
        )

        return formatter.render(entries)

    if arguments.command == "du":
        query = DiskUsageQuery(
            root=arguments.root,
            show_hidden=arguments.show_hidden,
            respect_gitignore=arguments.respect_gitignore,
        )
        total_size = DiskUsageUseCase.execute(query)

        return _format_size(total_size)

    raise ValueError(
        f"Unsupported command: {arguments.command}"
    )


def _format_size(size: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024

    return f"{value:.2f} TB"
