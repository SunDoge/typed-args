"""
metadata = {
    type: add_argument | add_parser
    args: arguments
    kwargs: keyword arguments
}
"""

from dataclasses import dataclass, field, Field
import argparse
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, TypeVar, Union
from argparse import Namespace, ArgumentParser, HelpFormatter
import functools
import sys
import dataclasses


_logger = logging.getLogger(__name__)

T = TypeVar('T')


def _get_dataclass_fields(cls) -> Dict[str, Field]:
    return getattr(cls, '__dataclass_fields__')


# def _get_metadata(cls, name: str, key: str):
#     return cls.__dataclass_fields__[name].metadata[key]


@dataclass
class TypedArgs:

    @classmethod
    def from_args(
        cls,
        args: Optional[List[str]] = None,
        namespace: Optional[Namespace] = None,
        parser: Optional[ArgumentParser] = None,
    ):

        if parser is None:
            parser = ArgumentParser()

        cls.add_arguments(parser, prefix='')

        args = parser.parse_args(args=args, namespace=namespace)

        typed_args = cls()
        typed_args.assign(args, prefix='')

        return typed_args

    @classmethod
    def from_known_args(
        cls: T,
        parser: Optional[ArgumentParser] = None,
        args: Optional[List[str]] = None,
        namespace: Optional[Namespace] = None
    ) -> Tuple[T, List[str]]:
        raise NotImplemented

    @classmethod
    def add_arguments(
        cls: T,
        parser: ArgumentParser,
        prefix: str = '',

    ):
        fields = _get_dataclass_fields(cls)
        for name, field in fields.items():

            # 嵌套
            dest = prefix + name
            _logger.debug('enter dest: %s', dest)

            if issubclass(field.type, TypedArgs):
                # 如果是嵌套的，就加上prefix之后解析
                _logger.debug('add recursive parser: %s', dest)
                field.type.add_arguments(parser, prefix=dest + '.')
            else:
                func_type = field.metadata.get('type', 'none')
                _logger.debug('get metadata=%s', field.metadata)
                if func_type == 'add_argument':
                    args: Sequence[str] = field.metadata['args']
                    kwargs = field.metadata['kwargs']
                    if len(args) > 0 and args[0].startswith('-'):
                        new_args = []
                        for a in args:
                            if a.startswith('--'):
                                new_args.append('--' + prefix + a[2:])
                            else:
                                new_args.append('-' + prefix + a[1:])
                        args = new_args

                    _logger.debug('add normal argument: %s', dest)
                    parser.add_argument(*args, dest=dest, **kwargs)
                elif func_type == 'none':
                    continue
                else:
                    raise Exception('no such type: {}'.format(func_type))

    def assign(self, args: Namespace, prefix: str = ''):
        fields = _get_dataclass_fields(self)
        for name, field in fields.items():
            dest = prefix + name

            if issubclass(field.type, TypedArgs):
                if field.default is not None:
                    field_args = field.default
                else:
                    field_args = field.type()
                field_args.assign(args, prefix=name + '.')
                setattr(self, name, field_args)
            else:
                func_type = field.metadata.get('type', 'none')

                if func_type == 'add_argument':
                    setattr(self, name, getattr(args, dest))
                elif func_type == 'none':
                    continue
                else:
                    raise Exception('no such type: {}'.format(func_type))


def add_argument(
    *flags: str,
    action=None,
    nargs=None,
    const=None,
    default=None,
    type=None,
    choices=None,
    required=None,
    help=None,
    metavar=None,
) -> Field:
    kwargs = locals()
    args = kwargs.pop('flags')
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return _add_argument(*args, **kwargs)


def _add_argument(*args, **kwargs) -> Field:
    """
    Args:
        action: str
    """
    metadata = {'type': 'add_argument', 'args': args, 'kwargs': kwargs}
    _logger.debug('metadata: %s', metadata)
    return field(default=None, metadata=metadata)
