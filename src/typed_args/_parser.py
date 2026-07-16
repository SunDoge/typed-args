from __future__ import annotations

import argparse
from typing import Optional, Sequence, TypeVar

from pydantic import BaseModel, ConfigDict

from ._builder import _resolve_optional_subcommands, build_parser

M = TypeVar("M", bound=BaseModel)
T = TypeVar("T", bound="TypedArgs")


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


def from_namespace(model: type[M], ns: argparse.Namespace) -> M:
    """Build a model instance from an already-parsed argparse Namespace.

    Use to extract a library's Args out of a host parser's namespace, after
    merging the Args with :func:`add_arguments` and parsing once yourself.
    The model's dotted dests are picked out; unrelated dests on the host parser
    are ignored (pydantic ``extra=ignore``).
    """
    tree = _resolve_optional_subcommands(_ns_to_tree(ns), model)
    return model.model_validate(tree)


def parse(
    model: type[M],
    argv: Optional[Sequence[str]] = None,
    *,
    parser: Optional[argparse.ArgumentParser] = None,
) -> M:
    p = build_parser(model, parser=parser)
    ns = p.parse_args(argv)
    return from_namespace(model, ns)


def parse_known_args(
    model: type[M],
    argv: Optional[Sequence[str]] = None,
    *,
    parser: Optional[argparse.ArgumentParser] = None,
) -> tuple[M, list[str]]:
    p = build_parser(model, parser=parser)
    ns, unknown = p.parse_known_args(argv)
    return from_namespace(model, ns), unknown


def add_arguments(
    parser: argparse.ArgumentParser, model: type[BaseModel]
) -> argparse.ArgumentParser:
    """Merge a model's arguments into an existing argparse parser (in place).

    Lets a library export an Args definition that a host app folds into its own
    parser. Parse once, then extract the Args instance with :func:`from_namespace`.

    Returns the same parser (for chaining).
    """
    return build_parser(model, parser=parser)


class TypedArgs(BaseModel):
    """Base class adding ``parse_args`` / ``parse_known_args`` classmethods.

    Parser config lives in ``model_config`` via :class:`ParserConfig`.
    ``use_attribute_docstrings`` defaults on, so a bare string literal after a
    field becomes its ``help`` text automatically.
    """

    model_config = ConfigDict(use_attribute_docstrings=True)

    @classmethod
    def parse_args(
        cls: type[T],
        argv: Optional[Sequence[str]] = None,
        *,
        parser: Optional[argparse.ArgumentParser] = None,
    ) -> T:
        return parse(cls, argv, parser=parser)

    @classmethod
    def parse_known_args(
        cls: type[T],
        argv: Optional[Sequence[str]] = None,
        *,
        parser: Optional[argparse.ArgumentParser] = None,
    ) -> tuple[T, list[str]]:
        return parse_known_args(cls, argv, parser=parser)
