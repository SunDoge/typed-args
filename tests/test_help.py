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


def test_subcommand_docstring_becomes_help(capsys):
    class Add(ta.TypedArgs):
        """add a file to the index"""

        cmd: Literal["add"] = "add"
        file: Annotated[str, ta.Arg()]

    class Root(ta.TypedArgs):
        subcommand: Annotated[Union[Add, Add], Field(discriminator="cmd")]

    # first line shows in the root Commands listing
    with pytest.raises(SystemExit):
        Root.parse_args(["--help"])
    out = capsys.readouterr().out
    assert "add a file to the index" in out

    # full docstring shows as the subparser description
    with pytest.raises(SystemExit):
        Root.parse_args(["add", "--help"])
    sub_out = capsys.readouterr().out
    assert "add a file to the index" in sub_out


def test_subcommand_multiline_docstring_only_first_in_help(capsys):
    class Add(ta.TypedArgs):
        """short summary line

        longer explanation that should appear in the subparser description
        but not in the one-line Commands listing help.
        """

        cmd: Literal["add"] = "add"
        file: Annotated[str, ta.Arg()]

    class Root(ta.TypedArgs):
        subcommand: Annotated[Union[Add, Add], Field(discriminator="cmd")]

    with pytest.raises(SystemExit):
        Root.parse_args(["--help"])
    root_out = capsys.readouterr().out
    assert "short summary line" in root_out
    assert "longer explanation" not in root_out

    with pytest.raises(SystemExit):
        Root.parse_args(["add", "--help"])
    sub_out = capsys.readouterr().out
    assert "short summary line" in sub_out
    assert "longer explanation" in sub_out


def test_subcommand_config_overrides_docstring(capsys):
    class Add(ta.TypedArgs):
        """docstring summary

        docstring details
        """

        model_config = ta.ParserConfig(
            subcommand_help="explicit summary",
            description="explicit details",
        )

        cmd: Literal["add"] = "add"

    class Root(ta.TypedArgs):
        subcommand: Annotated[Union[Add, Add], Field(discriminator="cmd")]

    with pytest.raises(SystemExit):
        Root.parse_args(["--help"])
    root_out = capsys.readouterr().out
    assert "explicit summary" in root_out
    assert "docstring summary" not in root_out

    with pytest.raises(SystemExit):
        Root.parse_args(["add", "--help"])
    sub_out = capsys.readouterr().out
    assert "explicit details" in sub_out
    assert "docstring details" not in sub_out


def test_subcommand_no_docstring_still_works(capsys):
    class Add(ta.TypedArgs):
        cmd: Literal["add"] = "add"
        file: Annotated[str, ta.Arg()]

    class Root(ta.TypedArgs):
        subcommand: Annotated[Union[Add, Add], Field(discriminator="cmd")]

    with pytest.raises(SystemExit):
        Root.parse_args(["--help"])
    out = capsys.readouterr().out
    assert "{add}" in out
