from __future__ import annotations

import argparse
from typing import Any, TypeVar, cast

from ._arg import Arg, Group, Mutex, Subparsers
from ._formatter import DefaultHelpFormatter
from ._schema import (
    DefaultNode,
    FieldEntry,
    ModelFieldsNode,
    Node,
    NullableNode,
    TaggedUnionNode,
    schema_of,
)

_UNSET = object()
M = TypeVar("M")

# argparse.ArgumentParser.__init__ params we honor from model_config.
_PARSER_KEYS = {
    "prog",
    "usage",
    "description",
    "epilog",
    "prefix_chars",
    "fromfile_prefix_chars",
    "argument_default",
    "conflict_handler",
    "add_help",
    "allow_abbrev",
    "exit_on_error",
    "formatter_class",
}


def _parser_kwargs(model: type) -> dict:
    cfg = getattr(model, "model_config", {}) or {}
    kw = {k: v for k, v in cfg.items() if k in _PARSER_KEYS}
    kw.setdefault("formatter_class", DefaultHelpFormatter)
    return kw


def _get_marker(fi, cls: type[M]) -> M | None:
    for m in fi.metadata:
        if isinstance(m, cls):
            return m
    return None


def _unwrap(node: Node) -> tuple[Node, Any]:
    """Strip default/nullable wrappers, carrying the default value out (if any)."""
    default = _UNSET
    # pyright does not narrow TypedDict discriminators inside loops, so cast at
    # each access after the type check.
    while node["type"] in ("default", "nullable"):
        if node["type"] == "default":
            d = cast(DefaultNode, node)
            if default is _UNSET:
                default = d["default"]
            node = d["schema"]
        else:
            n = cast(NullableNode, node)
            node = n["schema"]
    return node, default


def _opt_strings(name: str, arg: Arg | None) -> tuple[str, ...]:
    if arg and arg.option_strings:
        return arg.option_strings
    return (f"--{name.replace('_', '-')}",)


def _add(parser, name, dest, default, arg, *, extra=None, help=None):
    """Add one argument, merging Arg.kwargs over type-derived defaults.

    ``help`` is the fallback help text (Field description or attribute docstring);
    an explicit ``Arg(help=...)`` in ``arg.kwargs`` always wins.
    """
    kw = dict(extra) if extra else {}
    if arg:
        kw.update(arg.kwargs)
    if "dest" in kw:
        raise ValueError(
            "Arg(dest=...) is not supported: dest is derived from the field path "
            "(the link to the model field). Rename the field or use option strings."
        )
    if "help" not in kw and help:
        kw["help"] = help
    positional = (not arg or not arg.option_strings) and default is _UNSET
    if positional:
        kw.pop("required", None)
        kw.setdefault("default", None)
        parser.add_argument(dest=dest, **kw)
    else:
        if default is not _UNSET:
            kw.setdefault("default", default)
        parser.add_argument(*_opt_strings(name, arg), dest=dest, **kw)


def _emit(parser, model_cls, name, node: Node, default, fi, dest) -> None:
    if node["type"] == "tagged-union":
        _emit_subcommand(
            parser, node, dest,
            required=(default is _UNSET),
            subparsers=_get_marker(fi, Subparsers),
        )
        return
    if node["type"] == "model":
        group = _get_marker(fi, Group)
        mutex = _get_marker(fi, Mutex)
        if group:
            target = parser.add_argument_group(group.title, group.description)
        elif mutex:
            target = parser.add_mutually_exclusive_group(required=mutex.required)
        else:
            target = parser
        _add_fields(target, node["cls"], prefix=f"{dest}.")
        return
    arg = _get_marker(fi, Arg)
    help = fi.description
    if node["type"] == "bool":
        if arg and "action" in arg.kwargs:
            _add(parser, name, dest, default, arg, help=help)
        else:
            d = False if default is _UNSET else bool(default)
            _add(parser, name, dest, d, arg, extra={"action": "store_true"}, help=help)
        return
    if node["type"] == "literal":
        _add(parser, name, dest, default, arg, extra={"choices": node["expected"]}, help=help)
        return
    if node["type"] == "list":
        extra: dict = {}
        if not (arg and ("action" in arg.kwargs or "nargs" in arg.kwargs)):
            extra["nargs"] = "*"
        _add(parser, name, dest, default, arg, extra=extra, help=help)
        return
    # str / int / float / other scalars — pydantic coerces & validates
    _add(parser, name, dest, default, arg, help=help)


def _add_fields(
    parser, model_cls: type, prefix: str, skip: tuple[str, ...] = ()
) -> None:
    fields_node: ModelFieldsNode = schema_of(model_cls)
    for name, fi in model_cls.model_fields.items():
        if name in skip:
            continue
        entry: FieldEntry = fields_node["fields"][name]
        node, default = _unwrap(entry["schema"])
        _emit(parser, model_cls, name, node, default, fi, dest=prefix + name)


def _emit_subcommand(
    parser, node: TaggedUnionNode, dest, *, required: bool = True,
    subparsers: Subparsers | None = None,
) -> None:
    tag = node["discriminator"]
    kw: dict = {}
    if subparsers:
        for k in ("title", "description", "prog", "metavar"):
            v = getattr(subparsers, k)
            if v is not None:
                kw[k] = v
    subs = parser.add_subparsers(dest=f"{dest}.{tag}", required=required, **kw)
    for tagval, vnode in node["choices"].items():
        sp = subs.add_parser(tagval)
        _add_fields(sp, vnode["cls"], prefix=f"{dest}.", skip=(tag,))


def _resolve_optional_subcommands(tree: dict, model: type) -> dict:
    """For an optional subcommand (Optional[discriminated union] with a default),
    argparse writes the discriminator dest as None when no subcommand is chosen;
    collapse that subtree to None so the field takes its model default."""
    fields_node: ModelFieldsNode = schema_of(model)
    for name in model.model_fields:
        entry: FieldEntry = fields_node["fields"][name]
        node, default = _unwrap(entry["schema"])
        if node["type"] == "tagged-union" and default is not _UNSET:
            tu = cast(TaggedUnionNode, node)
            sub = tree.get(name)
            if isinstance(sub, dict) and sub.get(tu["discriminator"]) is None:
                tree[name] = None
    return tree


def build_parser(
    model: type, parser: argparse.ArgumentParser | None = None
) -> argparse.ArgumentParser:
    if parser is None:
        parser = argparse.ArgumentParser(**_parser_kwargs(model))
    fields_node: ModelFieldsNode = schema_of(model)
    for name, fi in model.model_fields.items():
        entry: FieldEntry = fields_node["fields"][name]
        node, default = _unwrap(entry["schema"])
        _emit(parser, model, name, node, default, fi, dest=name)
    return parser
