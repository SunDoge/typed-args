from typing import Annotated, Literal, Union

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


def test_global_after_subcommand(Root):
    r = Root.parse_args(["add", "x.txt", "--config", "c.yml", "-v"])
    assert r.common.config == "c.yml"
    assert r.common.verbose is True


def test_bad_subcommand_exits(Root):
    with pytest.raises(SystemExit):
        Root.parse_args(["bogus", "x"])
