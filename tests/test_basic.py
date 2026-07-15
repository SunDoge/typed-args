from typing import Annotated, Optional

import pytest

import typed_args as ta


def test_positional_and_option():
    class Args(ta.TypedArgs):
        foo: Annotated[str, ta.Arg("-f", "--foo")] = ""
        bar: Annotated[str, ta.Arg()]

    a = Args.parse_args(["BAR"])
    assert a.foo == "" and a.bar == "BAR"

    b = Args.parse_args(["BAR", "--foo", "FOO"])
    assert b.foo == "FOO" and b.bar == "BAR"


def test_missing_required_raises_system_exit():
    class Args(ta.TypedArgs):
        bar: Annotated[str, ta.Arg()]

    with pytest.raises(SystemExit):
        Args.parse_args(["--unknown"])


def test_optional_with_default():
    class Args(ta.TypedArgs):
        name: Annotated[str, ta.Arg("--name")] = "default"

    assert Args.parse_args([]).name == "default"
    assert Args.parse_args(["--name", "x"]).name == "x"


def test_bool_store_true():
    class Args(ta.TypedArgs):
        verbose: Annotated[bool, ta.Arg("-v", "--verbose")] = False

    assert Args.parse_args([]).verbose is False
    assert Args.parse_args(["-v"]).verbose is True


def test_store_const_via_action():
    class Args(ta.TypedArgs):
        mode: Annotated[str, ta.Arg("--fast", action="store_const", const="fast")] = (
            "slow"
        )

    assert Args.parse_args([]).mode == "slow"
    assert Args.parse_args(["--fast"]).mode == "fast"


def test_dashed_option_to_underscore_dest():
    class Args(ta.TypedArgs):
        dry_run: Annotated[bool, ta.Arg("--dry-run")] = False

    assert Args.parse_args(["--dry-run"]).dry_run is True


def test_optional_type_optional():
    class Args(ta.TypedArgs):
        opt: Annotated[Optional[str], ta.Arg("--opt")] = None

    assert Args.parse_args([]).opt is None
    assert Args.parse_args(["--opt", "v"]).opt == "v"
