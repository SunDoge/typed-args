import logging
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Union, Optional, Any, Iterable, List, Tuple

try:
    # Python 3.8
    from typing import get_origin, get_args
except ImportError:
    from .utils import get_origin, get_args

__version__ = '0.4.0'

logger = logging.getLogger(__name__)


@dataclass
class TypedArgs:
    # parser: ArgumentParser = field(default_factory=ArgumentParser)

    @classmethod
    def from_args(cls, args: Optional[List[str]] = None, namespace: Optional[Namespace] = None):
        typed_args = cls()
        typed_args._parse_args(typed_args.parser_factory(), args=args, namespace=namespace)
        return typed_args

    @classmethod
    def from_known_args(cls, args: Optional[List[str]] = None, namespace: Optional[Namespace] = None):
        typed_args = cls()
        args = typed_args._parse_known_args(typed_args.parser_factory(), args=args, namespace=namespace)
        return typed_args, args

    def parser_factory(self):
        return ArgumentParser()

    def _add_arguments(self, parser: ArgumentParser):
        for name, annotation in self.__dataclass_fields__.items():
            # There's no parser on self
            # if name == 'parser':
            #     continue
            self._add_argument(parser, name, annotation.type)

    def _add_argument(self, parser: ArgumentParser, name: str, annotation: Any):
        values: Union[PhantomAction, Tuple[PhantomAction]] = getattr(self, name)

        if type(values) != tuple:
            types = (annotation,)
            values = (values,)
        else:
            """
            List[Union[str, int]]
            """
            # types = annotation.__args__[0].__args__
            types = get_inner_types(annotation)
            # List[int, ...]
            if types[-1] == Ellipsis:
                types = (types[0],) * len(values)

        for argument_type, value in zip(types, values):
            # 如果不适用add_argument，则不parse
            if not isinstance(value, PhantomAction):
                continue

            kwargs = value.to_kwargs()
            """
            If there's no option_strings, it must be a position argument.
            For compatible, we get an empty tuple
            """
            args = kwargs.pop('option_strings', ())

            kwargs['dest'] = name  # 必定有dest

            is_position_argument = len(args) == 0

            origin = get_origin(argument_type)

            if origin is list:
                # We want inner type
                argument_type = get_args(argument_type)[0]

                # print('argument type: ', argument_type)

            if kwargs['action'] == 'store':

                # 不存在default的才需要判断optional
                if kwargs.get('default') is None:

                    if origin is Union:  # Optional
                        argument_type = get_args(argument_type)[0]  # Get first type
                        kwargs['required'] = False

                    elif origin is None:
                        if not is_position_argument:
                            kwargs['required'] = True

                kwargs['type'] = argument_type

            parser.add_argument(*args, **kwargs)

    def _parse_args(self, parser: ArgumentParser, args: Optional[List[str]] = None,
                    namespace: Optional[Namespace] = None):
        self._add_arguments(parser)
        parsed_args = parser.parse_args(args=args, namespace=namespace)
        self._update_arguments(parsed_args)

    def _parse_known_args(self, parser: ArgumentParser, args: Optional[List[str]] = None,
                          namespace: Optional[Namespace] = None):
        self._add_arguments(parser)
        parsed_args, args = parser.parse_known_args(
            args=args, namespace=namespace)
        self._update_arguments(parsed_args)
        return args

    def _update_arguments(self, parsed_args: Namespace):
        # for name in self.__dataclass_fields__.keys():
        #     # if name == 'parser':
        #     #     continue
        #     value = getattr(parsed_args, name)
        #     setattr(self, name, value)

        for name, value in parsed_args.__dict__.items():
            setattr(self, name, value)

        # del self.parser

        # self.parser = None


def get_inner_types(annotation):
    """
    List[Union[int, str]] -> get (int, str)
    """
    return annotation.__args__[0].__args__


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
        """
        Follow the argparse.add_argument rules
        """
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
    logger.debug('local = ', kwargs)

    # print('=' * 100)
    # print(kwargs)
    # print('=' * 100)

    return PhantomAction(**kwargs)
