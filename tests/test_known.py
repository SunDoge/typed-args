from typing import Annotated, Optional

import typed_args as ta


def test_parse_known_returns_unknown():
    class Args(ta.TypedArgs):
        name: Annotated[str, ta.Arg("--name")] = "x"

    parsed, unknown = Args.parse_known_args(["--name", "y", "--extra", "z"])
    assert parsed.name == "y"
    assert unknown == ["--extra", "z"]


def test_known_with_optional():
    class Args(ta.TypedArgs):
        opt: Annotated[Optional[str], ta.Arg("--opt")] = None

    parsed, unknown = Args.parse_known_args(["--opt", "v", "positional-leftover"])
    assert parsed.opt == "v"
    assert unknown == ["positional-leftover"]


def test_free_function_parse_known_args():
    class Args(ta.TypedArgs):
        x: Annotated[int, ta.Arg("-x")] = 0

    parsed, unknown = ta.parse_known_args(Args, ["-x", "3", "--stray"])
    assert parsed.x == 3
    assert unknown == ["--stray"]
