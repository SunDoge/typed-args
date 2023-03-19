import argparse
from typing import List, Optional, Sequence, Tuple, Type, TypeVar, overload, Callable
import dataclasses
import logging

from ._assigner import assign
from ._parser import parse


logger = logging.getLogger(__name__)

T = TypeVar('T')


def parse_args(
    klass: Type[T],
    parser: Optional[argparse.ArgumentParser] = None,
    args: Optional[Sequence[str]] = None,
    namespace:  Optional[argparse.Namespace] = None,
) -> T:
    assert dataclasses.is_dataclass(
        klass), "{} must be dataclass".format(klass)
    if not parser:
        parser = _make_parser(klass)
    parse(parser, klass)
    ns = parser.parse_args(args=args, namespace=namespace)
    opts = klass()
    assign(opts, ns)
    return opts


def parse_known_args(
    klass: Type[T],
    parser: Optional[argparse.ArgumentParser] = None,
    args: Optional[Sequence[str]] = None,
    namespace:  Optional[argparse.Namespace] = None,
) -> Tuple[T, List[str]]:
    assert dataclasses.is_dataclass(
        klass), "{} must be dataclass".format(klass)
    if not parser:
        parser = _make_parser(klass)
    parse(parser, klass)
    ns, unknown = parser.parse_known_args(args=args, namespace=namespace)
    opts = klass()
    assign(opts, ns)
    return opts, unknown


class TypedArgs:

    @classmethod
    def parse_args(
        cls: Type[T],
        args: Optional[Sequence[str]] = None,
        namespace:  Optional[argparse.Namespace] = None
    ) -> T:
        return parse_args(cls, args=args, namespace=namespace)

    @classmethod
    def parse_known_args(
        cls: Type[T],
        args: Optional[Sequence[str]] = None,
        namespace:  Optional[argparse.Namespace] = None
    ) -> Tuple[T, List[str]]:
        return parse_known_args(cls, args=args, namespace=namespace)


@overload
def argument_parser(
    prog: str = None,
    usage: str = None,
    description: str = None,
    epilog: str = None,
    parents: List[argparse.ArgumentParser] = None,
    formatter_class: argparse.HelpFormatter = None,
    prefix_chars: str = '-',
    fromfile_prefix_chars: str = None,
    argument_default=None,
    conflict_handler=None,
    add_help: bool = True,
    allow_abbrev: bool = True,
    exit_on_error: bool = True,
) -> Callable[[T], T]: ...


def argument_parser(**kwargs):

    def f(klass):
        def make_parser():
            return argparse.ArgumentParser(**kwargs)

        if not dataclasses.is_dataclass(klass):
            logger.debug("make %s a dataclass", klass)
            klass = dataclasses.dataclass(klass)

        setattr(klass, '__make_parser', make_parser)
        return klass

    return f


def _make_parser(klass):
    if hasattr(klass, '__make_parser'):
        parser = getattr(klass, '__make_parser')()
    else:
        parser = argparse.ArgumentParser()
    return parser
