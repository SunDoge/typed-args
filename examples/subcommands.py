"""Subcommands via pydantic discriminated unions + match dispatch."""

import sys
from typing import Annotated, Literal, Union

from pydantic import Field

import typed_args as ta


class GlobalArgs(ta.TypedArgs):
    verbose: Annotated[bool, ta.Arg("-v", "--verbose")] = False
    config: Annotated[str | None, ta.Arg("--config")] = None


class AddArgs(ta.TypedArgs):
    cmd: Literal["add"] = "add"
    file: Annotated[str, ta.Arg(help="file to add")]
    force: Annotated[bool, ta.Arg("--force")] = False


class RemoveArgs(ta.TypedArgs):
    cmd: Literal["remove"] = "remove"
    file: Annotated[str, ta.Arg(help="file to remove")]
    recursive: Annotated[bool, ta.Arg("-r", "--recursive")] = False


class Root(ta.TypedArgs):
    model_config = ta.ParserConfig(
        prog="gitlike",
        description="add/remove demo",
        formatter_class=ta.DefaultHelpFormatter,
    )
    common: GlobalArgs
    subcommand: Annotated[Union[AddArgs, RemoveArgs], Field(discriminator="cmd")]


def main(argv: list[str]) -> int:
    root = Root.parse_args(argv)
    match root.subcommand:
        case AddArgs(file=f, force=True):
            print(f"[add] force-add {f}")
        case AddArgs(file=f):
            print(f"[add] {f}")
        case RemoveArgs(file=f, recursive=True):
            print(f"[rm] recursive {f}")
        case RemoveArgs(file=f):
            print(f"[rm] {f}")
    if root.common.verbose:
        print("(verbose)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
