import argparse
import logging
from typing import List

from ._utils import SubcommandEnum, get_annotations, get_dataclass_fields

logger = logging.getLogger(__name__)


def _set_attr(x, paths: List[str], value):
    if len(paths) == 1:
        setattr(x, paths[0], value)
    elif len(paths) > 1:
        dataclass_fields = get_dataclass_fields(x)
        field = dataclass_fields.get(paths[0])
        action = field.metadata['action']
        if action == 'add_argument_group':
            group = getattr(x, paths[0])
            if group is None:
                group = field.type()
                setattr(x, paths[0], group)
            _set_attr(group, paths[1:], value)
        elif action == 'add_subparsers':
            annotations = get_annotations(field.type)
            key = paths[1]
            sub_command_enum: SubcommandEnum = getattr(x, paths[0])
            if sub_command_enum is None:
                sub_command = annotations[key]()
                sub_command_enum = field.type[key](sub_command)
                setattr(x, paths[0], sub_command_enum)
            else:
                sub_command = sub_command_enum.value
            _set_attr(sub_command, paths[2:], value)


def assign(x, ns: argparse.Namespace):
    kv = vars(ns)
    for key, value in kv.items():
        _set_attr(x, key.split('.'), value)
