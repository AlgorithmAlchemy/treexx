
# src/treexx/cli/main.py

import sys

from treexx.cli.args import parse_args
from treexx.cli.router import route


def main() -> int:
    try:
        arguments = parse_args()
        output = route(arguments)
    except (OSError, ValueError) as exc:
        print(f"treexx: error: {exc}", file=sys.stderr)
        return 1

    if output:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
