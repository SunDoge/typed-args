import argparse
import dataclasses
import enum
import inspect
import logging
from typing import DefaultDict, Generic, List, Optional, Set, Tuple, Type, TypeVar

from . import utils
from .api import Action, ActionType, get_action_from_field, has_action

_logger = logging.getLogger(__name__)

Memo = Set[str]
StrList = List[str]


T = TypeVar("T")


class ArgumentBuilder(Generic[T]):
    def __init__(
        self,
        klass: Type[T],
        parser: Optional[argparse.ArgumentParser] = None,
    ) -> None:

        if not parser:
            parser = argparse.ArgumentParser()

        memo: Memo = set()

        if issubclass(klass, enum.Enum):
            self._add_subparsers_to_parser(klass, parser, memo)
        else:
            self._add_multiple_arguments_to_parser(klass, parser, memo)

        self.parser = parser
        self.klass = klass

    def _add_subparsers_to_parser(
        self,
        klass: Type[enum.Enum],
        parser: argparse.ArgumentParser,
        memo: Memo,
    ):
        parent = inspect.getmro(klass)[1]
        if not issubclass(parent, enum.Enum):
            _logger.debug("add parent, %s", parent)
            self._add_multiple_arguments_to_parser(
                parent,
                parser,
                memo,
            )
        action_group: DefaultDict[Action, List[Action]] = DefaultDict(list)
        for name, member in utils.get_members(klass).items():
            action: Action = member.value
            action_group[action.context].append((name, action))

        assert len(action_group) == 1
        key = next(iter(action_group.keys()))
        if key:
            subparsers = parser.add_subparsers(**key.kwargs)
        else:
            subparsers = parser.add_subparsers()

        for name, action in action_group[key]:
            parser = subparsers.add_parser(*action.args, **action.kwargs)
            self._add_multiple_arguments_to_parser(action.klass, parser, memo)

    def _add_argument_to_parser(
        self,
        name: str,
        action: Action,
        parser: argparse.ArgumentParser,
    ):
        parser.add_argument(
            *action.args,
            dest=name,
            **action.kwargs,
        )

    def _add_multiple_arguments_to_parser(
        self,
        klass: Type,
        parser: argparse.ArgumentParser,
        memo: Memo,
    ):
        action_group: DefaultDict[Action, List[Tuple[str, Action]]] = DefaultDict(list)

        for name, field in utils.get_dataclass_fields(klass).items():
            if has_action(field):
                action = get_action_from_field(field)
                action_group[action.context].append((name, action))

        for group, actions in action_group.items():
            if group:
                parser.add_argument_group(
                    *group.args,
                    **group.kwargs,
                )

            for name, action in actions:
                if name not in memo:
                    self._add_argument_to_parser(name, action, parser)
                    memo.add(name)

    def parse_args(
        self,
        args: Optional[StrList] = None,
        namespace: Optional[argparse.Namespace] = None,
    ) -> T:
        parsed_args = self.parser.parse_args(args=args, namespace=namespace)
        return self.klass(**parsed_args.__dict__)

    def parse_known_args(
        self,
        args: Optional[StrList] = None,
        namespace: Optional[argparse.Namespace] = None,
    ) -> Tuple[T, StrList]:
        parsed_args, rest = self.parser.parse_known_args(args=args, namespace=namespace)
        return self.klass(**parsed_args.__dict__), rest


def parse_args(
    klass: Type[T],
    args: Optional[StrList] = None,
    namespace: Optional[argparse.Namespace] = None,
    parser: Optional[argparse.ArgumentParser] = None,
) -> T:
    return ArgumentBuilder(klass, parser=parser).parse_args(
        args=args, namespace=namespace
    )


def parse_known_args(
    klass: Type[T],
    args: Optional[StrList] = None,
    namespace: Optional[argparse.Namespace] = None,
    parser: Optional[argparse.ArgumentParser] = None,
) -> Tuple[T, StrList]:
    return ArgumentBuilder(klass, parser=parser).parse_known_args(
        args=args, namespace=namespace
    )
