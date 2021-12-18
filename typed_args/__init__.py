try:
    from dataclasses import dataclass
except ImportError as e:
    import warnings

    warnings.warn("Please `pip install dataclasses` if you are using Python 3.5 or 3.6")
    raise e

# from ._typed_args import TypedArgs, add_argument

from .api import add_argument, add_argument_group, add_parser, add_subparsers
from .core import ArgumentBuilder, parse_args, parse_known_args


__version__ = "0.6.0"

# __all__ = ["TypedArgs", "add_argument"]
