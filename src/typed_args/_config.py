from __future__ import annotations

import argparse
from typing import Optional

from pydantic import ConfigDict


class ParserConfig(ConfigDict, total=False):
    """Parser config that lives in ``model_config`` alongside pydantic config.

    Fields mirror ``argparse.ArgumentParser.__init__``. Mix freely with
    pydantic's own config keys, e.g.::

        model_config = ParserConfig(prog="cli", description="...", frozen=True)

    Custom keys are retained on the class and read by the builder; pydantic's
    own keys (``frozen``, ``str_strip_whitespace``, ...) still take effect.
    """

    prog: Optional[str]
    usage: Optional[str]
    description: Optional[str]
    epilog: Optional[str]
    prefix_chars: str
    fromfile_prefix_chars: Optional[str]
    argument_default: object
    conflict_handler: str
    add_help: bool
    allow_abbrev: bool
    exit_on_error: bool
    formatter_class: type[argparse.HelpFormatter]
