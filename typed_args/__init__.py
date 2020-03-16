import logging
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field
from typing import Union, Optional, Any, Iterable, List, Tuple

try:
    # Python 3.8
    from typing import get_origin, get_args
except ImportError:
    from .utils import get_origin, get_args

__version__ = '0.3.3'

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
            if name == 'parser':
                continue
            self.add_argument(name, annotation)

    def add_argument(self, name: str, annotation: Any):
        values: Union[PhantomAction, Tuple[PhantomAction]] = getattr(self, name)

        if type(values) != tuple:
            types = (annotation,)
            values = (values,)
        else:
            types = annotation.__args__[0].__args__
            if types[-1] == Ellipsis:
                types = (types[0],) * len(values)

        for argument_type, value in zip(types, values):
            kwargs = value.to_kwargs()
            args = kwargs.pop('option_strings', ())

            kwargs['dest'] = name  # 必定有dest

            is_position_argument = len(args) == 0

            origin = get_origin(argument_type)

            if origin is list:
                argument_type = get_args(argument_type)[0]

                print('argument type: ', argument_type)

            if kwargs['action'] == 'store':

                # 不存在default的才需要判断optional
                if kwargs.get('default', None) is None:

                    if origin is Union:  # Optional
                        argument_type = get_args(argument_type)[0]
                        kwargs['required'] = False
                    elif origin is None:
                        if not is_position_argument:
                            kwargs['required'] = True

                kwargs['type'] = argument_type

            self.parser.add_argument(*args, **kwargs)

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
            if name == 'parser':
                continue
            value = getattr(parsed_args, name)
            setattr(self, name, value)


@dataclass
class PhantomAction:
    option_strings: Tuple[str, ...]
    action: str = 'store'
    nargs: Union[int, str, None] = None
    const: Any = None
    default: Any = None
    choices: Optional[Iterable] = None
    required: Optional[bool] = None
    help: Optional[str] = None
    metavar: Optional[str] = None

    def to_kwargs(self):
        kwargs = self.__dict__.copy()

        if len(self.option_strings) == 0:
            # position argument is always required
            del kwargs['required']

        if self.action.startswith('store_'):
            del kwargs['nargs']
            del kwargs['choices']

            if self.action in ['store_true', 'store_false']:
                del kwargs['metavar']
                del kwargs['const']
                del kwargs['default']

        elif self.action == 'append_const':
            del kwargs['nargs']
            del kwargs['choices']

        elif self.action == 'count':
            del kwargs['nargs']
            del kwargs['choices']
            del kwargs['const']
            del kwargs['metavar']

        elif self.action == 'help':
            del kwargs['dest']
            del kwargs['default']

            del kwargs['nargs']
            del kwargs['choices']
            del kwargs['const']
            del kwargs['metavar']
            del kwargs['required']

        elif self.action == 'version':
            del kwargs['dest']
            del kwargs['default']

            del kwargs['nargs']
            del kwargs['choices']
            del kwargs['const']
            del kwargs['metavar']
            del kwargs['required']

        elif self.action == 'parsers':
            raise NotImplemented()

        return kwargs


def add_argument(
        *option_strings: Union[str, Tuple[str, ...]],
        action: str = 'store',  # in argparse, default action is 'store'
        nargs: Union[int, str, None] = None,
        const: Optional[Any] = None,
        default: Optional[Any] = None,
        choices: Optional[Iterable] = None,
        required: Optional[bool] = None,
        help: Optional[str] = None,
        metavar: Optional[str] = None,
):
    """

    :param option_strings:
    :param action:
    :param nargs:
    :param const:
    :param default:
    :param choices:
    :param required:
    :param help:
    :param metavar:
    :return:
    """
    kwargs = locals()
    LOGGER.debug('local = ', kwargs)

    # print('=' * 100)
    # print(kwargs)
    # print('=' * 100)

    return PhantomAction(**kwargs)
