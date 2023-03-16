import dataclasses
import enum
from typing import Dict, Any, Type, Optional
from types import DynamicClassAttribute
import argparse


class EnumMember:
    name: str
    value: Dict[str, Any]


def get_dataclass_fields(x) -> Dict[str, dataclasses.Field]:
    return getattr(x, '__dataclass_fields__')


def get_members(x) -> Dict[str, EnumMember]:
    return getattr(x, '__members__')


def get_annotations(x) -> Dict[str, Type]:
    return getattr(x, '__annotations__')


def has_dataclass_fields(x):
    return hasattr(x, '__dataclass_fields__')


class _Subcommand:

    def __init__(self, value, name: Optional[str] = None) -> None:
        if not hasattr(self, "_value_"):
            self._value_ = value

        if not hasattr(self, "_name_") and name is not None:
            self._name_ = name

    @DynamicClassAttribute
    def name(self) -> str:
        return self._name_

    @DynamicClassAttribute
    def value(self):
        return self._value_

    def __call__(self, value):
        return _Subcommand(value, name=self.name)

    def __repr__(self) -> str:
        return f'<_SubCommand {self.name}: {self.value}>'

    def __eq__(self, other: '_Subcommand') -> bool:
        # ic(isinstance(self, type(rhs)))
        # ic(isinstance(rhs, type(self)))

        # FIXME: confuse me
        return isinstance(self, type(other)) and self.name == other.name


class SubcommandEnum(_Subcommand, enum.Enum):
    """
    Black magic!
    """
    pass


class DefaultHelpFormatter(argparse.HelpFormatter):

    def _get_default_metavar_for_optional(self, action: argparse.Action) -> str:
        return action.dest.split('.')[-1].upper()

    def _get_default_metavar_for_positional(self, action: argparse.Action) -> str:
        return action.dest.split('.')[-1]
