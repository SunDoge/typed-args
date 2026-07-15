import argparse
from typing import Annotated

import pytest

import typed_args as ta


def test_prog_and_description_from_config(capsys):
    class Args(ta.TypedArgs):
        model_config = ta.ParserConfig(prog="myprog", description="a demo cli")

    with pytest.raises(SystemExit):
        Args.parse_args(["--help"])
    out = capsys.readouterr().out
    assert "myprog" in out
    assert "a demo cli" in out


def test_formatter_strips_dotted_dest(capsys):
    class G(ta.TypedArgs):
        verbose: Annotated[bool, ta.Arg("-v", "--verbose")] = False

    class Root(ta.TypedArgs):
        common: G

    with pytest.raises(SystemExit):
        Root.parse_args(["--help"])
    out = capsys.readouterr().out
    assert "COMMON" not in out  # DefaultHelpFormatter strips the dotted prefix
    assert "--verbose" in out


def test_parser_passthrough_escape_hatch():
    class Args(ta.TypedArgs):
        name: Annotated[str, ta.Arg("--name")] = "x"

    custom = argparse.ArgumentParser(prog="custom")
    a = Args.parse_args(["--name", "y"], parser=custom)
    assert a.name == "y"
    assert custom.prog == "custom"


def test_pydantic_config_mixes_with_parser_config():
    class Args(ta.TypedArgs):
        model_config = ta.ParserConfig(frozen=True, str_strip_whitespace=True)
        name: Annotated[str, ta.Arg("--name")] = "x"

    a = Args.parse_args(["--name", "  hi  "])
    assert a.name == "hi"
    with pytest.raises(Exception):
        a.name = "changed"
