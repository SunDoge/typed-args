from typing import Annotated, Literal, Union

import pytest
from pydantic import Field

import typed_args as ta


def test_subcommands_listed_in_help(capsys):
    class Add(ta.TypedArgs):
        cmd: Literal["add"] = "add"
        file: Annotated[str, ta.Arg(help="file to add")]

    class Remove(ta.TypedArgs):
        cmd: Literal["remove"] = "remove"

    class Root(ta.TypedArgs):
        subcommand: Annotated[Union[Add, Remove], Field(discriminator="cmd")]

    with pytest.raises(SystemExit):
        Root.parse_args(["--help"])
    out = capsys.readouterr().out
    assert "{add,remove}" in out


def test_arg_help_text_shown(capsys):
    class Args(ta.TypedArgs):
        name: Annotated[str, ta.Arg("--name", help="your name")] = ""

    with pytest.raises(SystemExit):
        Args.parse_args(["--help"])
    out = capsys.readouterr().out
    assert "your name" in out


def test_attribute_docstring_becomes_help(capsys):
    class Args(ta.TypedArgs):
        file: Annotated[str, ta.Arg()]
        "the file to add"

    with pytest.raises(SystemExit):
        Args.parse_args(["--help"])
    out = capsys.readouterr().out
    assert "the file to add" in out


def test_arg_help_overrides_docstring(capsys):
    class Args(ta.TypedArgs):
        file: Annotated[str, ta.Arg(help="explicit")]
        "docstring text"

    with pytest.raises(SystemExit):
        Args.parse_args(["--help"])
    out = capsys.readouterr().out
    assert "explicit" in out
    assert "docstring text" not in out
