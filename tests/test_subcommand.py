from typing import Annotated, Literal, Optional, Union

import pytest
from pydantic import Field

import typed_args as ta


class Globals(ta.TypedArgs):
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


@pytest.fixture
def Root() -> type:
    """Composed root with global args + a discriminated-union subcommand."""
    Sub = Annotated[Union[AddArgs, RemoveArgs], Field(discriminator="cmd")]

    class Root(ta.TypedArgs):
        common: Globals
        subcommand: Sub

    return Root


def test_add(Root):
    r = Root.parse_args(["add", "foo.txt"])
    assert isinstance(r.subcommand, AddArgs)
    assert r.subcommand.file == "foo.txt"
    assert r.subcommand.force is False
    assert r.common.verbose is False


def test_remove(Root):
    r = Root.parse_args(["remove", "bar.txt", "-r"])
    assert isinstance(r.subcommand, RemoveArgs)
    assert r.subcommand.recursive is True


def test_global_before_subcommand(Root):
    r = Root.parse_args(["--verbose", "add", "x.txt", "--force"])
    assert r.common.verbose is True
    assert r.subcommand.force is True


def test_global_after_subcommand_rejected(Root):
    # globals must precede the subcommand (argparse behavior); flags after the
    # subcommand are not recognized.
    with pytest.raises(SystemExit):
        Root.parse_args(["add", "x.txt", "--config", "c.yml", "-v"])


def test_bad_subcommand_exits(Root):
    with pytest.raises(SystemExit):
        Root.parse_args(["bogus", "x"])


def test_optional_subcommand():
    class Add(ta.TypedArgs):
        cmd: Literal["add"] = "add"
        file: Annotated[str, ta.Arg()]

    class Root(ta.TypedArgs):
        subcommand: Optional[Annotated[Union[Add, Add], Field(discriminator="cmd")]] = (
            None
        )

    assert Root.parse_args([]).subcommand is None
    r = Root.parse_args(["add", "x"])
    assert isinstance(r.subcommand, Add) and r.subcommand.file == "x"


def test_subparsers_section_in_help(capsys):
    class Add(ta.TypedArgs):
        cmd: Literal["add"] = "add"
        file: Annotated[str, ta.Arg()]

    class Root(ta.TypedArgs):
        subcommand: Annotated[
            Union[Add, Add],
            Field(discriminator="cmd"),
            ta.Subparsers(title="Commands", description="pick one"),
        ] = None

    with pytest.raises(SystemExit):
        Root.parse_args(["--help"])
    out = capsys.readouterr().out
    assert "Commands" in out
    assert "pick one" in out
