try:
    from dataclasses import dataclass
except ImportError as e:
    import warnings
    warnings.warn(
        'Please `pip install dataclasses` if you are using Python 3.5 or 3.6'
    )
    raise e


from ._core import parse_args, parse_known_args, argument_parser, TypedArgs
from ._parser import add_argument, add_argument_group, add_parser, add_subparsers
from ._utils import SubcommandEnum, DefaultHelpFormatter
from argparse import SUPPRESS, OPTIONAL, ZERO_OR_MORE, ONE_OR_MORE, REMAINDER

__version__ = "0.6.1"

__all__ = [
    'dataclass',
    'parse_args', 'parse_known_args', 'argument_parser', 'TypedArgs',
    'add_argument', 'add_argument_group', 'add_parser', 'add_subparsers',
    'SubcommandEnum', 'DefaultHelpFormatter',
    'SUPPRESS', 'OPTIONAL', 'ZERO_OR_MORE', 'ONE_OR_MORE', 'REMAINDER',
]
