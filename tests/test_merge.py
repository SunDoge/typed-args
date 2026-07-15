"""Integrating a library-exported Args into a host argparse parser."""

import argparse
from typing import Annotated

import typed_args as ta


class LibArgs(ta.TypedArgs):
    host: Annotated[str, ta.Arg("--host", help="db host")] = "localhost"
    port: Annotated[int, ta.Arg("-p")] = 5432
    tls: Annotated[bool, ta.Arg("--tls")] = False


def test_add_arguments_merges_into_host_parser():
    user = argparse.ArgumentParser(prog="app")
    user.add_argument("--config", dest="user_config", default=None)
    ta.add_arguments(user, LibArgs)

    ns = user.parse_args(["--config", "c.yml", "--host", "db", "-p", "6543", "--tls"])

    lib = ta.from_namespace(LibArgs, ns)
    assert lib.host == "db"
    assert lib.port == 6543
    assert lib.tls is True
    # host's own field is still accessible on the shared namespace
    assert ns.user_config == "c.yml"


def test_add_arguments_defaults_when_flags_absent():
    user = argparse.ArgumentParser()
    ta.add_arguments(user, LibArgs)
    ns = user.parse_args([])
    lib = ta.from_namespace(LibArgs, ns)
    assert lib == LibArgs()


def test_add_arguments_returns_same_parser():
    user = argparse.ArgumentParser()
    assert ta.add_arguments(user, LibArgs) is user


def test_nested_field_composition():
    """A library Args embedded as a field of a host TypedArgs."""

    class HostArgs(ta.TypedArgs):
        config: Annotated[str, ta.Arg("--config")] = "default"
        lib: LibArgs

    a = HostArgs.parse_args(
        ["--config", "c.yml", "--host", "db", "-p", "6543", "--tls"]
    )
    assert a.config == "c.yml"
    assert isinstance(a.lib, LibArgs)
    assert a.lib.host == "db"
    assert a.lib.port == 6543
    assert a.lib.tls is True

    # absent lib flags -> nested instance built from LibArgs defaults
    b = HostArgs.parse_args([])
    assert b.config == "default"
    assert b.lib == LibArgs()
