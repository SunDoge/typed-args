from typing import Any, Dict, Optional, Tuple, Type, Union, overload
import argparse
import dataclasses
from enum import Enum, auto
import logging

_logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--fuck", default="fuck")
parser.add_argument_group()
parser.add_subparsers


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


def get_action_from_field(field: dataclasses.Field) -> Action:
    return field.metadata["action"]


@overload
def add_argument(*flags: str) -> dataclasses.Field:
    ...


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


def add_argument_group(description: Optional[str] = None):
    action = Action(ActionType.AddArgumentGroup, (),
                    dict(description=description))
    return dataclasses.field(metadata=dict(action=action))


def add_parser():
    pass


def add_subparsers():
    pass
