import argparse
import dataclasses
import enum
import logging
from typing import overload, TypeVar, Type, Optional, Sequence

from ._utils import get_annotations, get_dataclass_fields, get_members

logger = logging.getLogger(__name__)


def _parse_dataclass(parser: argparse.ArgumentParser, x, prefix: str = ''):
    fields = get_dataclass_fields(x)

    for name, field in fields.items():
        action = field.metadata.get('action')
        dest = prefix + name
        if action == 'add_argument':
            args = field.metadata.get('args')
            kwargs = field.metadata.get('kwargs')
            parser.add_argument(*args, dest=dest, **kwargs)
        elif action == 'add_argument_group':
            group = parser.add_argument_group(title=name)
            _parse_dataclass(group, field.type, prefix=dest + '.')
        elif action == 'add_subparsers':
            args = field.metadata.get('args')
            kwargs = field.metadata.get('kwargs')
            subparsers = parser.add_subparsers(*args, **kwargs)
            _parse_enum(subparsers, field.type, prefix=dest + '.')


def _parse_enum(subparsers: argparse._SubParsersAction, x, prefix: str = ''):
    members = get_members(x)
    annotations = get_annotations(x)

    for member in members.values():
        name = member.value.get('name')
        kwargs = member.value.get('kwargs')
        dest = prefix + member.name
        parser = subparsers.add_parser(name, **kwargs)
        _parse_dataclass(parser, annotations.get(
            member.name), prefix=dest + '.')


def parse(parser: argparse.ArgumentParser, x):
    if issubclass(x, enum.Enum):
        subparsers = parser.add_subparsers()
        _parse_enum(subparsers, x)
    else:
        _parse_dataclass(parser, x)


T = TypeVar('T')


@overload
def add_argument(
    *option_strings: str,
    action: str = None,
    nargs: str = None,
    const: T = None,
    default: T = None,
    type: Type[T] = None,
    choices: Sequence[T] = None,
    required: bool = None,
    help: str = None,
    metavar: str = None,
) -> T: ...


def add_argument(*args, **kwargs):
    return dataclasses.field(default=None, metadata=dict(args=args, kwargs=kwargs, action='add_argument'))


def add_argument_group(*args, **kwargs):
    return dataclasses.field(default=None, metadata=dict(args=args, kwargs=kwargs, action='add_argument_group'))


def add_subparsers(*args, **kwargs):
    return dataclasses.field(default=None, metadata=dict(args=args, kwargs=kwargs, action='add_subparsers'))


def add_parser(name: str, **kwargs):
    return dict(name=name, kwargs=kwargs)
