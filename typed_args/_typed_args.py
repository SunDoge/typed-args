"""
metadata = {
    type: add_argument | add_parser
    args: arguments
    kwargs: keyword arguments
}
"""

import dataclasses
import inspect
import logging
from argparse import Action, ArgumentParser, Namespace
from collections.abc import Container
from dataclasses import Field, dataclass
from enum import Enum
from typing import (Any, Callable, Dict, List, Optional, Sequence, Tuple, Type,
                    TypeVar, Union)

_logger = logging.getLogger(__name__)

T = TypeVar('T', bound='TypedArgs')


def _get_dataclass_fields(cls) -> Dict[str, Field]:
    return getattr(cls, '__dataclass_fields__')


@dataclass
class TypedArgs:

    @classmethod
    def from_args(
        cls: Type[T],
        args: Optional[List[str]] = None,
        namespace: Optional[Namespace] = None,
        parser: Optional[ArgumentParser] = None,
    ) -> T:

        if parser is None:
            parser = ArgumentParser()

        cls._add_arguments(parser, prefix='')

        parsed_args: Namespace = parser.parse_args(
            args=args, namespace=namespace)

        typed_args = cls()
        typed_args._assign(parsed_args, prefix='')

        return typed_args

    @classmethod
    def from_known_args(
        cls: Type[T],
        args: Optional[List[str]] = None,
        namespace: Optional[Namespace] = None,
        parser: Optional[ArgumentParser] = None,
    ) -> Tuple[T, List[str]]:
        if parser is None:
            parser = ArgumentParser()

        cls._add_arguments(parser, prefix='')

        parsed_args, unknown = parser.parse_known_args(
            args=args, namespace=namespace)

        typed_args = cls()
        typed_args._assign(parsed_args, prefix='')

        return typed_args, unknown

    @classmethod
    def _add_arguments(
        cls,
        parser: ArgumentParser,
        prefix: str = '',
    ):
        fields = _get_dataclass_fields(cls)
        for name, field in fields.items():

            # 嵌套
            dest = prefix + name
            # _logger.debug('enter dest: %s', dest)

            if inspect.isclass(field.type) and issubclass(field.type, TypedArgs):
                # 如果是嵌套的，就加上prefix之后解析
                # _logger.debug('add recursive parser: %s', dest)
                field.type._add_arguments(parser, prefix=dest + '.')
            else:
                func_type = field.metadata.get('type', 'none')
                # _logger.debug('get metadata=%s', field.metadata)
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

                    # _logger.debug('add normal argument: %s', dest)
                    parser.add_argument(*args, dest=dest, **kwargs)
                elif func_type == 'none':
                    continue
                else:
                    raise Exception('no such type: {}'.format(func_type))

    def _assign(self, args: Namespace, prefix: str = ''):
        fields = _get_dataclass_fields(self)
        for name, field in fields.items():
            dest = prefix + name

            if inspect.isclass(field.type) and issubclass(field.type, TypedArgs):
                if field.default is not None:
                    field_args = field.default
                else:
                    field_args = field.type()
                field_args._assign(args, prefix=name + '.')
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
    action: Union[str, Type[Action]] = None,
    nargs: Union[str, int] = None,
    const: Any = None,
    default: Any = None,
    type: Callable[[str], Any] = None,
    choices: Container = None,  # to support `is in`
    required: bool = None,
    help: str = None,
    metavar: str = None,
) -> Any:
    kwargs = locals()
    args = kwargs.pop('flags')

    # The parser.add_argument only accept args with value
    # We use default value None to filter out the unused args
    # add_argument(*args, **kwargs) 有复杂的规则
    # 为了避免手动处理这些规则，采用过滤 None 的方式来过滤没有使用的参数
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return _add_argument(*args, **kwargs)


def _add_argument(*args, **kwargs) -> Field:
    """
    Args:
        action: str
    """
    metadata = {'type': 'add_argument', 'args': args, 'kwargs': kwargs}
    default = kwargs.get('default', None)

    if isinstance(default, (list, dict, set)):
        _logger.debug(
            'mutable object cannot be dataclass default attribute, make default_factory'
        )

        field_default = dataclasses.MISSING
        def default_factory(): return default
    else:
        field_default = default
        default_factory = dataclasses.MISSING

    # _logger.debug('metadata: %s', metadata)
    return dataclasses.field(
        default=field_default,
        default_factory=default_factory,
        metadata=metadata
    )


def add_parser():
    pass


def _add_parser(**kwargs):
    pass


def _get_members(cls) -> Dict[str, Enum]:
    return getattr(cls, '__members__')


class SubTypedArgs(TypedArgs, Enum):

    @classmethod
    def _add_arguments(cls, parser: ArgumentParser, prefix: str):
        subparsers = parser.add_subparsers()
        members = _get_members(cls)

        for name, member in members.items():
            name = prefix + name
            subparser = subparsers.add_parser(name)
            member.value._add_arguments(subparser)
