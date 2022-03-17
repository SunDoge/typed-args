from typing import Any, Dict, Optional, Tuple, Type, Union, overload
import argparse
import dataclasses
from enum import Enum, auto
import logging

_logger = logging.getLogger(__name__)

# parser = argparse.ArgumentParser()
# parser.add_argument("--fuck", default="fuck")
# parser.add_argument_group()
# parser.add_subparsers


class ActionType(Enum):
    AddArgument = auto()
    AddArgumentGroup = auto()
    AddSubparsers = auto()
    AddParser = auto()


@dataclasses.dataclass
class Action:
    type: ActionType
    args: Tuple
    kwargs: Dict
    klass: Optional[Type] = None
    context: Optional["Action"] = None


def get_action_from_field(field: dataclasses.Field) -> Action:
    # _logger.debug('field: %s', field)
    return field.metadata["action"]


def has_action(field: dataclasses.Field) -> bool:
    return 'action' in field.metadata

# @overload
# def add_argument(*flags: str) -> dataclasses.Field:
#     ...


def add_argument(*args, **kwargs):

    action = Action(
        ActionType.AddArgument,
        args,
        kwargs,
    )

    default = kwargs.get("default")

    if isinstance(default, (list, dict, set)):
        _logger.debug(
            "mutable object cannot be dataclass default attribute, make default_factory"
        )

        def default_factory():
            default

        return dataclasses.field(
            default_factory=default_factory,
            metadata=dict(action=action),
        )
    else:
        return dataclasses.field(default=default, metadata=dict(action=action))



class ArgumentGroup:

    def __init__(self, action: Action) -> None:
        self.action = action

    def add_argument(self, *args, **kwargs):
        field = add_argument(*args, **kwargs)
        get_action_from_field(field).context = self.action
        return field


def add_argument_group(description: Optional[str] = None):
    action = Action(ActionType.AddArgumentGroup, (), dict(description=description))
    return dataclasses.field(metadata=dict(action=action))


def add_parser(klass: Type, *args, **kwargs):
    action = Action(
        ActionType.AddParser,
        args,
        kwargs,
        klass=klass,
    )
    return action


class Subparsers:
    def __init__(self, action: Action) -> None:
        self.action = action

    def add_parser(self, klass: Type, **kwargs):
        action = add_parser(klass, **kwargs)
        action.context = self.action
        return action


def add_subparsers(**kwargs) -> Subparsers:
    action = Action(
        ActionType.AddSubparsers,
        (),
        kwargs,
    )
    return Subparsers(action)
