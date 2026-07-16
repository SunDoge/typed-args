"""Mutually exclusive groups via the Mutex marker."""
from typing import Annotated

import pytest

import typed_args as ta


class Opts(ta.TypedArgs):
    foo: Annotated[str, ta.Arg("--foo")] = ""
    bar: Annotated[str, ta.Arg("--bar")] = ""


class Cli(ta.TypedArgs):
    opts: Annotated[Opts, ta.Mutex()]


def test_mutex_one_flag_ok():
    c = Cli.parse_args(["--foo", "f"])
    assert c.opts.foo == "f" and c.opts.bar == ""


def test_mutex_two_flags_rejected():
    with pytest.raises(SystemExit):
        Cli.parse_args(["--foo", "f", "--bar", "b"])


def test_mutex_required_rejects_none():
    class O2(ta.TypedArgs):
        a: Annotated[str, ta.Arg("--a")] = ""
        b: Annotated[str, ta.Arg("--b")] = ""

    class C2(ta.TypedArgs):
        opts: Annotated[O2, ta.Mutex(required=True)]

    with pytest.raises(SystemExit):
        C2.parse_args([])


def test_mutex_required_accepts_one():
    class O2(ta.TypedArgs):
        a: Annotated[str, ta.Arg("--a")] = ""
        b: Annotated[str, ta.Arg("--b")] = ""

    class C2(ta.TypedArgs):
        opts: Annotated[O2, ta.Mutex(required=True)]

    assert C2.parse_args(["--a", "x"]).opts.a == "x"
