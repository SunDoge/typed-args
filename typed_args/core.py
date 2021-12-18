import argparse
import enum
import inspect
from typing import Generic, Optional, Set, Type, TypeVar
import typing
import logging

from .api import ActionType, _Action
from . import utils

_logger = logging.getLogger(__name__)

T = TypeVar("T")
Memo = Set[str]


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
            items = iter(utils.get_members(klass).items())
            # TODO, state machine for subparsers


    def _add_argument_to_parser(
        self,
    ):
        pass

    def _add_multiple_arguments_to_parser(
        self,
        klass,
        parser: argparse.ArgumentParser,
        memo: Memo,
    ):
        pass
