import argparse
import dataclasses
import enum
import logging
from typing import overload, TypeVar, Type, Sequence, Union, Dict
import ast
import inspect
import textwrap
import typing


from ._utils import get_annotations, get_dataclass_fields, get_members

logger = logging.getLogger(__name__)


def _parse_dataclass(parser: argparse.ArgumentParser, x, prefix: str = ""):
    _parse_attribute_docstring(x)
    fields = get_dataclass_fields(x)

    for name, field in fields.items():
        action = field.metadata.get("action")
        dest = prefix + name
        if action == "add_argument":
            args = field.metadata.get("args")
            kwargs = field.metadata.get("kwargs")
            parser.add_argument(*args, dest=dest, **kwargs)
        elif action == "add_argument_group":
            group = parser.add_argument_group(title=name)
            _parse_dataclass(group, field.type, prefix=dest + ".")
        elif action == "add_subparsers":
            args = field.metadata.get("args")
            kwargs = field.metadata.get("kwargs")
            subparsers = parser.add_subparsers(*args, **kwargs)
            _parse_enum(subparsers, field.type, prefix=dest + ".")


def _parse_enum(subparsers: argparse._SubParsersAction, x, prefix: str = ""):
    members = get_members(x)
    annotations = get_annotations(x)

    for member in members.values():
        name = member.value.get("name")
        kwargs = member.value.get("kwargs")
        dest = prefix + member.name
        parser = subparsers.add_parser(name, **kwargs)
        _parse_dataclass(parser, annotations.get(member.name), prefix=dest + ".")


def parse(parser: argparse.ArgumentParser, x):
    if issubclass(x, enum.Enum):
        subparsers = parser.add_subparsers()
        _parse_enum(subparsers, x)
    else:
        _parse_dataclass(parser, x)


def _parse_attribute_docstring(x):
    source = inspect.getsource(x)
    """
    https://stackoverflow.com/questions/41882261/reduce-indentation-of-nested-functions-in-python-code-generation
    We dedent the code to support class in function
    """
    source = textwrap.dedent(source)
    module = ast.parse(source)
    class_def = typing.cast(ast.ClassDef, module.body[0])
    ann_assign_indices = [
        i for i, x in enumerate(class_def.body) if isinstance(x, ast.AnnAssign)
    ]
    num_keys = len(class_def.body)
    res = {}
    """
    class ClassDef:
        AnnAssign target = value
        Expr(Constant)
    """
    for ann_assign_idx in ann_assign_indices:
        expr_idx = ann_assign_idx + 1
        if expr_idx >= num_keys:
            continue
        expr = class_def.body[expr_idx]
        if not isinstance(expr, ast.Expr):
            continue
        ann_assign = typing.cast(ast.AnnAssign, class_def.body[ann_assign_idx])
        key: str = ann_assign.target.id
        constant: ast.Constant = expr.value
        value: str = constant.value
        # TODO: we may have to strip the value
        res[key] = value

    dataclass_fields = get_dataclass_fields(x)
    for key, value in res.items():
        field = dataclass_fields[key]
        if field.metadata.get("action") == "add_argument":
            kwargs = typing.cast(Dict, field.metadata.get("kwargs"))
            if "help" not in kwargs:
                kwargs["help"] = value


T = TypeVar("T")
R = TypeVar("R")


@overload
def add_argument(
    *option_strings: str,
    action: str = ...,
    nargs: str | int = ...,
    const: T = ...,
    default: Union[T, str] = ...,
    type: Type[T] = ...,
    choices: Sequence[T] = ...,
    required: bool = ...,
    help: str = ...,
    metavar: str = ...,
) -> R: ...


def add_argument(*args, **kwargs):
    return dataclasses.field(
        default=None, metadata=dict(args=args, kwargs=kwargs, action="add_argument")
    )


@overload
def add_argument_group(
    title: str = ...,
    description: str = ...,
) -> dataclasses.Field: ...


def add_argument_group(*args, **kwargs):
    return dataclasses.field(
        default=None,
        metadata=dict(args=args, kwargs=kwargs, action="add_argument_group"),
    )


@overload
def add_subparsers(
    title: str = ...,
    description: str = ...,
    prog: str = ...,
    parser_class: Type[argparse.ArgumentParser] = ...,
    action=...,
    required: bool = ...,
    help: str = ...,
    metavar: str = ...,
) -> R: ...


def add_subparsers(*args, **kwargs):
    return dataclasses.field(
        default=None, metadata=dict(args=args, kwargs=kwargs, action="add_subparsers")
    )


@overload
def add_parser(
    name: str,
    prog: str = ...,
    aliases: Sequence[str] = ...,
) -> dict: ...


def add_parser(name: str, **kwargs):
    return dict(name=name, kwargs=kwargs)
