import argparse
from typing import List
from ._utils import has_dataclass_fields, get_dataclass_fields, get_annotations
import enum
import logging
from icecream import ic
from ._utils import SubcommandEnum

logger = logging.getLogger(__name__)


def _set_attr(x, paths: List[str], value):
    ic(locals())
    if len(paths) == 1:
        setattr(x, paths[0], value)
        ic('after setattr', x)
    elif len(paths) > 1:
        dataclass_fields = get_dataclass_fields(x)
        field = dataclass_fields.get(paths[0])
        action = field.metadata['action']
        if action == 'add_argument_group':
            if getattr(x, paths[0]) is None:
                group = field.type()
                setattr(x, paths[0], group)
            else:
                group = getattr(x, paths[0])
            _set_attr(group, paths[1:], value)
        elif action == 'add_subparsers':
            annotations = get_annotations(field.type)
            key = paths[1]
            if getattr(x, paths[0]) is None:
                sub_command = annotations[key]()
                sub_command_enum = field.type[key](sub_command)
                setattr(x, paths[0], sub_command_enum)
            else:
                sub_command_enum: SubcommandEnum = getattr(x, paths[0])
                sub_command = sub_command_enum.value
            _set_attr(sub_command, paths[2:], value)


def _assign_dataclass(x, ns: argparse.Namespace):
    kv = vars(ns)
    for key, value in kv.items():
        _set_attr(x, key.split('.'), value)


def _set_enum_attr(x, paths: List[str], value):
    pass
