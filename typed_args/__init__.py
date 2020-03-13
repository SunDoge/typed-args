import logging
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field
from typing import Union, Optional, Any, Iterable, List, Tuple
import typing

__version__ = '0.3.0'

LOGGER = logging.getLogger(__name__)


@dataclass
class TypedArgs:
    parser: ArgumentParser = field(default_factory=ArgumentParser)

    @classmethod
    def from_args(cls, args: Optional[List[str]] = None, namespace: Optional[Namespace] = None):
        typed_args = cls()
        typed_args.parse_args(args=args, namespace=namespace)
        return typed_args

    @classmethod
    def from_known_args(cls, args: Optional[List[str]] = None, namespace: Optional[Namespace] = None):
        typed_args = cls()
        typed_args.parse_known_args(args=args, namespace=namespace)
        return typed_args

    def add_arguments(self):
        for name, annotation in self.__annotations__.items():
            self.add_argument(name, annotation)

    def add_argument(self, name: str, annotation: Any):
        local_variables = getattr(self, name)

        # if multiple actions are added to one dest, we will have more than on actions
        # 统一把action变成iterable

        if isinstance(annotation, type(List)):
            if annotation._name == 'List':
                """
                List存在两种情况，append_const需要add两次，List[Union[T1, T2]]
                append，只add一次
                """
                if type(local_variables) == tuple:
                    # 绝对不会是positional
                    types = annotation.__args__[0].__args__

                    for t, v in zip(types, local_variables):
                        v = v.default_factory()

                        v['kwargs']['dest'] = name

                        # append_const不能输入type
                        if not v['kwargs']['action'].endswith('const'):
                            v['kwargs']['type'] = t

                        self.parser.add_argument(*v['args'], **v['kwargs'])
                else:
                    # positional不能输入dest
                    if local_variables['args'][0].startswith('-'):
                        local_variables['kwargs']['dest'] = name
                        
                    local_variables['kwargs']['type'] = annotation.__args__[0]
                    self.parser.add_argument(
                        *local_variables['args'], **local_variables['kwargs'])
        else:
            if local_variables['args'][0].startswith('-'):
                local_variables['kwargs']['dest'] = name
            local_variables['kwargs']['type'] = annotation
            self.parser.add_argument(
                *local_variables['args'], **local_variables['kwargs'])

    def parse_args(self, args: Optional[List[str]] = None, namespace: Optional[Namespace] = None):
        self.add_arguments()
        parsed_args = self.parser.parse_args(args=args, namespace=namespace)
        self.update_arguments(parsed_args)

    def parse_known_args(self, args: Optional[List[str]] = None, namespace: Optional[Namespace] = None):
        self.add_arguments()
        parsed_args, _ = self.parser.parse_known_args(
            args=args, namespace=namespace)
        self.update_arguments(parsed_args)

    def update_arguments(self, parsed_args: Namespace):
        for name in self.__annotations__.keys():
            value = getattr(parsed_args, name)
            setattr(self, name, value)


# @dataclass
# class PhantomAction:
#     option_strings: Tuple[str, ...]
#     action: Optional[str] = None
#     nargs: Union[int, str, None] = None
#     const: Any = None
#     default: Any = None
#     choices: Optional[Iterable] = None
#     required: Optional[bool] = None
#     help: Optional[str] = None
#     metavar: Optional[str] = None


def add_argument(*args, **kwargs):

    local_variables = locals()

    LOGGER.debug('locals = %s', local_variables)

    return field(default_factory=lambda: local_variables)
