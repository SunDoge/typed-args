"""typed-args: typed CLI argument parsing with pydantic models (Python clap)."""

from ._arg import Arg
from ._config import ParserConfig
from ._formatter import DefaultHelpFormatter
from ._parser import TypedArgs, add_arguments, from_namespace, parse, parse_known_args

__all__ = [
    "Arg",
    "TypedArgs",
    "ParserConfig",
    "parse",
    "parse_known_args",
    "add_arguments",
    "from_namespace",
    "DefaultHelpFormatter",
]
