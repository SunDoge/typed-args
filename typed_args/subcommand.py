import argparse
import dataclasses
import enum
import inspect
import logging
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Callable,
    Container,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

_logger = logging.getLogger(__name__)

# The name of an attribute on the class where we store the Field
# objects.  Also used to check if a class is a Data Class.
DATACLASS_FIELDS = "__dataclass_fields__"

MEMBERS = "__members__"


StrList = List[str]
Memo = Set[dataclasses.Field]


class _Dataclass:

    __dataclass_fields__: Dict[str, dataclasses.Field]


class ActionType(enum.Enum):
    AddArgument = enum.auto()
    AddArgumentGroup = enum.auto()
    AddParser = enum.auto()
    AddSubparsers = enum.auto()


def _get_dataclass_fields(x: _Dataclass) -> Dict[str, dataclasses.Field]:
    return getattr(x, "__dataclass_fields__")


def _get_members(x: Type[Enum]) -> Dict[str, Enum]:
    return getattr(x, "__members__")


def _remove_none_in_kwargs(kwargs: Dict) -> Dict:
    return {k: v for k, v in kwargs.items() if v is not None}


def _add_arguments_to_parser(
    typed_args: _Dataclass,
    parser: argparse.ArgumentParser,
    memo: Memo,
):
    for name, field in _get_dataclass_fields(typed_args).items():
        if field not in memo:
            _add_argument_to_parser(name, field, parser)
            memo.add(field)
        else:
            _logger.debug("%s is in memo, will no be added to parser", field)


def _add_argument_to_parser(
    name,
    field: dataclasses.Field,
    parser: argparse.ArgumentParser,
):
    args = field.metadata["args"]
    kwargs = field.metadata["kwargs"]
    dest = name
    parser.add_argument(*args, dest=dest, **kwargs)


def _add_subparsers_to_parser(
    typed_args: Type[Enum],
    parser: argparse.ArgumentParser,
    memo: Memo,
):
    parent = inspect.getmro(typed_args)[1]
    if parent is not enum.Enum:
        _logger.debug("add parent, %s", parent)
        _add_arguments_to_parser(cast(_Dataclass, parent), parser, memo)

    items = iter(_get_members(typed_args).items())
    _, member = next(items)
    metadata: Dict = member.value
    if metadata["type"] == ActionType.AddSubparsers:
        subparsers = parser.add_subparsers(**metadata["kwargs"])
    else:
        subparsers = parser.add_subparsers()
        items = iter(_get_members(typed_args).items())

    for name, member in items:
        member_metadata = member.value
        parser = subparsers.add_parser(name, **member_metadata["kwargs"])
        _add_arguments_to_parser(
            member_metadata["typed_args"],
            parser,
            memo,
        )


def add_argument(
    *flags: str,
    action: Union[str, Type[argparse.Action]] = None,
    nargs: Union[str, int] = None,
    const: Any = None,
    default: Any = None,
    type: Callable[[str], Any] = None,
    choices: Container = None,  # to support `is in`
    required: bool = None,
    help: str = None,
    metavar: str = None,
):
    args = flags
    kwargs = dict(
        action=action,
        nargs=nargs,
        const=const,
        default=default,
        type=type,
        choices=choices,
        required=required,
        help=help,
        metavar=metavar,
    )
    kwargs = _remove_none_in_kwargs(kwargs)
    field_default = kwargs.get("default", None)

    metadata = {"type": ActionType.AddArgument, "args": args, "kwargs": kwargs}

    if isinstance(field_default, (list, dict, set)):
        _logger.debug(
            "mutable object cannot be dataclass default attribute, "
            "change to default_factory"
        )

        def default_factory():
            return field_default

        return dataclasses.field(default_factory=default_factory, metadata=metadata)
    else:
        return dataclasses.field(default=field_default, metadata=metadata)


def add_subparsers(
    title: Optional[str] = None,
    description: Optional[str] = None,
    prog: Optional[str] = None,
    parser_class: argparse.ArgumentParser = None,
    action: argparse.Action = None,
    dest: Optional[str] = None,
    required: bool = None,
    help: Optional[str] = None,
    metavar: Optional[str] = None,
):
    kwargs = dict(
        title=title,
        description=description,
        prog=prog,
        parser_class=parser_class,
        action=action,
        dest=dest,
        required=required,
        help=help,
        metavar=metavar,
    )
    kwargs = _remove_none_in_kwargs(kwargs)
    metadata = {
        "type": ActionType.AddSubparsers,
        "kwargs": kwargs,
    }
    return metadata


def add_parser(typed_args: Type, **kwargs):
    metadata = {
        "type": ActionType.AddParser,
        "typed_args": typed_args,
        "kwargs": kwargs,
    }
    return metadata


def add_argument_group(name: str):
    pass


T = TypeVar("T")


class ArgumentBuilder(Generic[T]):
    def __init__(
        self,
        typed_args: Type[T],
        parser: Optional[argparse.ArgumentParser] = None,
    ) -> None:
        parser = parser if parser else argparse.ArgumentParser()
        memo: Memo = set()

        if issubclass(typed_args, enum.Enum):
            _add_subparsers_to_parser(typed_args, parser, memo)
        else:
            _add_arguments_to_parser(cast(_Dataclass, typed_args), parser, memo)

        self.parser = parser
        self.typed_args = typed_args

    def parse_args(
        self,
        args: Optional[StrList] = None,
        namespace: Optional[argparse.Namespace] = None,
    ) -> T:
        parsed_args = self.parser.parse_args(
            args=args,
            namespace=namespace,
        )
        return self.typed_args(**parsed_args.__dict__)

    def parse_known_args(
        self,
        args: Optional[StrList],
        namespace: Optional[argparse.Namespace],
    ) -> Tuple[T, StrList]:
        parsed_args, rest_args = self.parser.parse_known_args(
            args=args,
            namespace=namespace,
        )
        return self.typed_args(**parsed_args.__dict__), rest_args


def _init_logger():
    logging.basicConfig(level=logging.DEBUG)


def main1():
    _init_logger()

    @dataclass
    class Args:
        foo: str = add_argument("--foo")
        bar: str = add_argument("--bar", default="foobar")

    builder = ArgumentBuilder(Args)
    args = builder.parse_args()
    print(args)


def main2():
    _init_logger()

    @dataclass
    class A:
        common: str = add_argument("--common")

    @dataclass
    class Foo(A):
        foo: str = add_argument("--foo")

    @dataclass
    class Bar(A):
        bar: str = add_argument("--bar")

    class Args(A, enum.Enum):
        # _ = add_subparsers()
        foo = add_parser(Foo)
        bar = add_parser(Bar)

    builder = ArgumentBuilder(Args)
    args = builder.parse_args()
    print(args)


if __name__ == "__main__":
    # main1()
    main2()
