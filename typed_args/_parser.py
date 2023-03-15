import argparse
from typing import Type, TypeVar, Dict, List, Any, Optional
import dataclasses
from icecream import ic
from ._utils import get_annotations, get_dataclass_fields, get_members
import logging
import enum

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
            subparsers = parser.add_subparsers()
            _parse_enum(subparsers, field.type, prefix=dest + '.')


def _parse_enum(subparsers: argparse._SubParsersAction, x, prefix: str = ''):
    members = get_members(x)
    annotations = get_annotations(x)

    for member in members.values():
        name = member.value.get('name')
        dest = prefix + member.name
        parser = subparsers.add_parser(name)
        _parse_dataclass(parser, annotations.get(
            member.name), prefix=dest + '.')


def parse(parser: argparse.ArgumentParser, x):
    if issubclass(x, enum.Enum):
        subparsers = parser.add_subparsers()
        _parse_enum(subparsers, x)
    else:
        _parse_dataclass(parser, x)


def add_argument(*args, **kwargs):
    return dataclasses.field(default=None, metadata=dict(args=args, kwargs=kwargs, action='add_argument'))


def add_argument_group(*args, **kwargs):
    return dataclasses.field(default=None, metadata=dict(args=args, kwargs=kwargs, action='add_argument_group'))


def add_subparsers(*args, **kwargs):
    return dataclasses.field(default=None, metadata=dict(args=args, kwargs=kwargs, action='add_subparsers'))


def add_parser(name: str):
    return dict(name=name)


class DefaultHelpFormatter(argparse.HelpFormatter):

    def _get_default_metavar_for_optional(self, action: argparse.Action) -> str:
        return action.dest.split('.')[-1].upper()

    def _get_default_metavar_for_positional(self, action: argparse.Action) -> str:
        return action.dest.split('.')[-1]
