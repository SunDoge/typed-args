"""Typed views over pydantic's core schema.

The builder reads pydantic's core schema as dicts. These TypedDicts give the
node variants we touch real types so a checker can narrow on the ``type``
discriminator (``Literal[...]``) and validate the per-variant keys. ``schema_of``
insulates the access from pydantic's own (over-complex) core-schema union typing
via ``Any`` + ``cast``.

Only the node shapes the builder actually reads are modeled; extra keys pydantic
puts on these dicts are harmlessly present and unmodeled.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict, Union, cast

from pydantic import BaseModel, TypeAdapter


class FieldEntry(TypedDict):
    schema: "Node"
    metadata: list[Any]


class ModelFieldsNode(TypedDict):
    type: Literal["model-fields"]
    fields: dict[str, FieldEntry]


class ModelNode(TypedDict):
    type: Literal["model"]
    cls: type[BaseModel]
    schema: "Node"


class TaggedUnionNode(TypedDict):
    type: Literal["tagged-union"]
    discriminator: str
    choices: dict[str, ModelNode]


class DefaultNode(TypedDict):
    type: Literal["default"]
    default: Any
    schema: "Node"


class NullableNode(TypedDict):
    type: Literal["nullable"]
    schema: "Node"


class LiteralNode(TypedDict):
    type: Literal["literal"]
    expected: list[Any]


class LeafNode(TypedDict):
    type: Literal["bool", "str", "int", "float", "list"]


Node = Union[
    ModelFieldsNode,
    ModelNode,
    TaggedUnionNode,
    DefaultNode,
    NullableNode,
    LiteralNode,
    LeafNode,
]


def schema_of(model: type[BaseModel]) -> ModelFieldsNode:
    """The ``model-fields`` node of a BaseModel's core schema."""
    raw: Any = TypeAdapter(model).core_schema
    return cast(ModelFieldsNode, raw["schema"])
