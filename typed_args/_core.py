import argparse
from typing import Generic, List, Optional, Sequence, Tuple, Type, TypeVar
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
    if not parser:
        parser = argparse.ArgumentParser()
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
    if not parser:
        parser = argparse.ArgumentParser()
    parse(parser, klass)
    ns, unknown = parser.parse_known_args(args=args, namespace=namespace)
    opts = klass()
    assign(opts, ns)
    return opts, unknown


class _Parsable(Generic[T]):

    @classmethod
    def parse_args(cls, args: Optional[Sequence[str]] = None, namespace:  Optional[argparse.Namespace] = None) -> T:
        pass

    @classmethod
    def parse_known_args(cls, args: Optional[Sequence[str]] = None, namespace:  Optional[argparse.Namespace] = None) -> Tuple[T, List[str]]:
        pass


def argument_parser(**kwargs):

    def f(klass: Type[T]) -> _Parsable[T]:
        def _make_parser():
            return argparse.ArgumentParser(**kwargs)

        def _parse_args(args=None, namespace=None):
            parser = _make_parser()
            return parse_args(klass, parser=parser, args=args, namespace=namespace)

        def _parse_known_args(args=None, namespace=None):
            parser = _make_parser()
            return parse_known_args(klass, parser=parser, args=args, namespace=namespace)

        if not dataclasses.is_dataclass(klass):
            logger.debug("make %s a dataclass", klass)
            klass = dataclasses.dataclass(klass)

        setattr(klass, 'parse_args', _parse_args)
        setattr(klass, 'parse_known_args', _parse_known_args)
        return klass

    return f
