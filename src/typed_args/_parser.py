from __future__ import annotations

import argparse
from typing import Any, Optional, Sequence

from pydantic import BaseModel, ConfigDict, TypeAdapter

from ._builder import _unwrap, build_parser


def _ns_to_tree(ns: argparse.Namespace) -> dict:
    """Reconstruct a nested dict from dotted-dest namespace keys."""
    tree: dict = {}
    for key, value in vars(ns).items():
        parts = key.split(".")
        d = tree
        for p in parts[:-1]:
            d = d.setdefault(p, {})
        d[parts[-1]] = value
    return tree


def _fill_absent_models(tree: dict, model: type[BaseModel]) -> dict:
    """Globals use ``default=SUPPRESS`` so absent flags write nothing. A nested
    model field (e.g. ``common``) that received no flags is then absent and would
    be treated as required. Fill it with ``{}`` so pydantic builds it from the
    sub-model's own field defaults."""
    fields_node = TypeAdapter(model).core_schema["schema"]
    for name in model.model_fields:
        node, _ = _unwrap(fields_node["fields"][name]["schema"])
        if node["type"] == "model" and name not in tree:
            tree[name] = {}
    return tree


def parse(
    model: type[BaseModel],
    argv: Optional[Sequence[str]] = None,
    *,
    parser: Optional[argparse.ArgumentParser] = None,
) -> Any:
    p = build_parser(model, parser=parser)
    ns = p.parse_args(argv)
    tree = _fill_absent_models(_ns_to_tree(ns), model)
    return model.model_validate(tree)


def parse_known_args(
    model: type[BaseModel],
    argv: Optional[Sequence[str]] = None,
    *,
    parser: Optional[argparse.ArgumentParser] = None,
):
    p = build_parser(model, parser=parser)
    ns, unknown = p.parse_known_args(argv)
    tree = _fill_absent_models(_ns_to_tree(ns), model)
    return model.model_validate(tree), unknown


class TypedArgs(BaseModel):
    """Base class adding ``parse_args`` / ``parse_known_args`` classmethods.

    Parser config lives in ``model_config`` via :class:`TypedArgsConfig`.
    ``use_attribute_docstrings`` defaults on, so a bare string literal after a
    field becomes its ``help`` text automatically.
    """

    model_config = ConfigDict(use_attribute_docstrings=True)

    @classmethod
    def parse_args(
        cls,
        argv: Optional[Sequence[str]] = None,
        *,
        parser: Optional[argparse.ArgumentParser] = None,
    ):
        return parse(cls, argv, parser=parser)

    @classmethod
    def parse_known_args(
        cls,
        argv: Optional[Sequence[str]] = None,
        *,
        parser: Optional[argparse.ArgumentParser] = None,
    ):
        return parse_known_args(cls, argv, parser=parser)
