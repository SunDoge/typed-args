from __future__ import annotations

import argparse
from typing import Any, cast

from ._arg import Arg
from ._formatter import DefaultHelpFormatter
from ._schema import (
    DefaultNode,
    FieldEntry,
    ModelFieldsNode,
    ModelNode,
    Node,
    NullableNode,
    TaggedUnionNode,
    schema_of,
)

_UNSET = object()

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


def _get_arg(fi) -> Arg | None:
    for m in fi.metadata:
        if isinstance(m, Arg):
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


def _add(parser, name, dest, default, arg, *, extra=None, suppress=False, help=None):
    """Add one argument, merging Arg.kwargs over type-derived defaults.

    ``suppress`` forces ``default=argparse.SUPPRESS`` so an absent flag does not
    write the dest — used for globals shared across main + subparsers to avoid the
    argparse subparser default-clobber; pydantic's model default fills the gap.
    ``help`` is the fallback help text (Field description or attribute docstring);
    an explicit ``Arg(help=...)`` in ``arg.kwargs`` always wins.
    """
    kw = dict(extra) if extra else {}
    if arg:
        kw.update(arg.kwargs)
    if "help" not in kw and help:
        kw["help"] = help
    positional = (not arg or not arg.option_strings) and default is _UNSET
    if positional:
        kw.pop("required", None)
        kw.setdefault("default", None)
        parser.add_argument(dest=dest, **kw)
    else:
        if suppress:
            kw["default"] = argparse.SUPPRESS
        elif default is not _UNSET:
            kw.setdefault("default", default)
        parser.add_argument(*_opt_strings(name, arg), dest=dest, **kw)


def _emit(
    parser, model_cls, name, node: Node, default, arg, dest, suppress=False, help=None
) -> None:
    if node["type"] == "tagged-union":
        _emit_subcommand(parser, node, dest)
        return
    if node["type"] == "model":
        _add_fields(parser, node["cls"], prefix=f"{dest}.", suppress=suppress)
        return
    if node["type"] == "bool":
        if arg and "action" in arg.kwargs:
            _add(parser, name, dest, default, arg, suppress=suppress, help=help)
        else:
            d = False if default is _UNSET else bool(default)
            _add(
                parser,
                name,
                dest,
                d,
                arg,
                extra={"action": "store_true"},
                suppress=suppress,
                help=help,
            )
        return
    if node["type"] == "literal":
        _add(
            parser,
            name,
            dest,
            default,
            arg,
            extra={"choices": node["expected"]},
            suppress=suppress,
            help=help,
        )
        return
    if node["type"] == "list":
        extra: dict = {}
        if not (arg and ("action" in arg.kwargs or "nargs" in arg.kwargs)):
            extra["nargs"] = "*"
        _add(
            parser, name, dest, default, arg, extra=extra, suppress=suppress, help=help
        )
        return
    # str / int / float / other scalars — pydantic coerces & validates
    _add(parser, name, dest, default, arg, suppress=suppress, help=help)


def _add_fields(
    parser, model_cls: type, prefix: str, skip: tuple[str, ...] = (), suppress=False
) -> None:
    fields_node: ModelFieldsNode = schema_of(model_cls)
    for name, fi in model_cls.model_fields.items():
        if name in skip:
            continue
        entry: FieldEntry = fields_node["fields"][name]
        node, default = _unwrap(entry["schema"])
        # fi.description holds Field(description=...) OR, when use_attribute_docstrings
        # is on, the attribute docstring (Field wins). Arg(help=...) overrides both.
        help = fi.description
        _emit(
            parser,
            model_cls,
            name,
            node,
            default,
            _get_arg(fi),
            dest=prefix + name,
            suppress=suppress,
            help=help,
        )


def _emit_subcommand(parser, node: TaggedUnionNode, dest, parents=()) -> None:
    tag = node["discriminator"]
    subs = parser.add_subparsers(dest=f"{dest}.{tag}", required=True)
    for tagval, vnode in node["choices"].items():
        sp = subs.add_parser(
            tagval, parents=list(parents), formatter_class=DefaultHelpFormatter
        )
        _add_fields(sp, vnode["cls"], prefix=f"{dest}.", skip=(tag,))


def _root_globals_parent(model: type) -> argparse.ArgumentParser | None:
    """Root nested-model fields (e.g. `common`) become a shared parent parser
    so they work both before and after the subcommand."""
    fields_node: ModelFieldsNode = schema_of(model)
    parent = None
    for name, fi in model.model_fields.items():
        node, _ = _unwrap(fields_node["fields"][name]["schema"])
        if node["type"] == "model":
            if parent is None:
                parent = argparse.ArgumentParser(
                    add_help=False, formatter_class=DefaultHelpFormatter
                )
            _add_fields(parent, node["cls"], prefix=f"{name}.", suppress=True)
    return parent


def build_parser(
    model: type, parser: argparse.ArgumentParser | None = None
) -> argparse.ArgumentParser:
    globals_parent = _root_globals_parent(model)

    if parser is None:
        kw = _parser_kwargs(model)
        if globals_parent is not None:
            kw.setdefault("parents", []).append(globals_parent)
        parser = argparse.ArgumentParser(**kw)
    elif globals_parent is not None:
        # user-supplied parser: add globals directly (before-subcommand support)
        fields_node: ModelFieldsNode = schema_of(model)
        for name, fi in model.model_fields.items():
            node, _ = _unwrap(fields_node["fields"][name]["schema"])
            if node["type"] == "model":
                _add_fields(parser, node["cls"], prefix=f"{name}.", suppress=True)

    fields_node = schema_of(model)
    for name, fi in model.model_fields.items():
        node, default = _unwrap(fields_node["fields"][name]["schema"])
        if node["type"] == "model":
            continue  # handled via globals_parent / direct add above
        if node["type"] == "tagged-union":
            parents = [globals_parent] if globals_parent else []
            _emit_subcommand(parser, node, name, parents=parents)
            continue
        _emit(
            parser,
            model,
            name,
            node,
            default,
            _get_arg(fi),
            dest=name,
            help=fi.description,
        )

    return parser
