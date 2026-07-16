"""Argument groups via the Group marker (display-only sectioning)."""
from typing import Annotated

import typed_args as ta


class DbArgs(ta.TypedArgs):
    host: Annotated[str, ta.Arg("--host")] = "localhost"
    port: Annotated[int, ta.Arg("-p")] = 5432


class LogArgs(ta.TypedArgs):
    level: Annotated[str, ta.Arg("--level")] = "info"


class Cli(ta.TypedArgs):
    general: Annotated[str, ta.Arg("--general")] = "x"
    db: Annotated[DbArgs, ta.Group("Database", "database settings")]
    log: Annotated[LogArgs, ta.Group("Logging")]


def test_group_parse_and_reconstruct():
    cli = Cli.parse_args(
        ["--general", "g", "--host", "db", "-p", "6543", "--level", "debug"]
    )
    assert cli.general == "g"
    assert cli.db.host == "db"
    assert cli.db.port == 6543
    assert cli.log.level == "debug"


def test_group_defaults_when_absent():
    cli = Cli.parse_args([])
    assert cli.db == DbArgs()
    assert cli.log == LogArgs()


def test_group_section_in_help(capsys):
    import pytest

    with pytest.raises(SystemExit):
        Cli.parse_args(["--help"])
    out = capsys.readouterr().out
    assert "Database" in out
    assert "database settings" in out
    assert "Logging" in out
    # metavar is stripped (DefaultHelpFormatter), not dotted
    assert "DB.HOST" not in out
