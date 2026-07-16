from __future__ import annotations

import argparse
from typing import Any, Callable, Iterable

__all__ = ["Arg", "Group", "Subparsers", "Mutex"]


class Arg:
    """Argparse-passthrough marker attached to a model field via ``Annotated[T, Arg(...)]``.

    ``option_strings`` (``-f``, ``--foo``) make the field an optional; omit them for a
    positional. The keyword args mirror :meth:`argparse.ArgumentParser.add_argument` and
    overlay the type-derived defaults (``bool``→``store_true``, ``Literal``→``choices``,
    ``list``→``nargs="*"``). Precedence for ``help``:
    ``Arg(help=...)`` > ``Field(description=...)`` > attribute docstring.

    Params left ``None`` are treated as unspecified and not forwarded, so the
    type-derived default applies. Anything beyond the params below is accepted via
    ``**kwargs`` and passed straight to ``add_argument`` (e.g. for custom ``Action``s).

    ``dest`` is **not** accepted: it is derived from the field path, which is the link
    between the argparse namespace and the model field — overriding it would desync the
    two. To change the CLI attribute, rename the field; to change the flag name, use
    option strings.
    """

    __slots__ = ("option_strings", "kwargs")

    def __init__(
        self,
        *option_strings: str,
        action: str | type[argparse.Action] | None = None,
        nargs: int | str | None = None,
        const: Any = None,
        default: Any = None,
        type: Callable[[str], Any] | None = None,
        choices: Iterable[Any] | None = None,
        required: bool | None = None,
        help: str | None = None,
        metavar: str | tuple[str, ...] | None = None,
        **kwargs: Any,
    ) -> None:
        self.option_strings = option_strings
        for k, v in {
            "action": action,
            "nargs": nargs,
            "const": const,
            "default": default,
            "type": type,
            "choices": choices,
            "required": required,
            "help": help,
            "metavar": metavar,
        }.items():
            if v is not None:
                kwargs[k] = v
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return f"Arg({self.option_strings!r}, {self.kwargs!r})"


class Group:
    """Marker placing a nested model's arguments in a titled argparse group.

    Display-only: the arguments still live on the same parser/namespace with their
    dotted dests (so ``model_validate`` reconstructs the nested instance unchanged);
    only ``--help`` renders them under a section header. Attached via
    ``Annotated[SomeArgs, Group("Title", "optional description")]``.
    """

    __slots__ = ("title", "description")

    def __init__(
        self, title: str | None = None, description: str | None = None
    ) -> None:
        self.title = title
        self.description = description

    def __repr__(self) -> str:
        return f"Group(title={self.title!r}, description={self.description!r})"


class Subparsers:
    """Marker customizing the subcommand section (``add_subparsers`` metadata).

    Attached to a discriminated-union field, e.g. ::
        ``Annotated[Union[A, B], Field(discriminator="cmd"), Subparsers(title="Commands")]``.
    Only set fields are forwarded to ``add_subparsers``.
    """

    __slots__ = ("title", "description", "prog", "metavar")

    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        prog: str | None = None,
        metavar: str | None = None,
    ) -> None:
        self.title = title
        self.description = description
        self.prog = prog
        self.metavar = metavar

    def __repr__(self) -> str:
        return (
            f"Subparsers(title={self.title!r}, description={self.description!r}, "
            f"prog={self.prog!r}, metavar={self.metavar!r})"
        )


class Mutex:
    """Marker placing a nested model's arguments in a mutually exclusive group.

    At most one of the group's flags may be given on the command line (argparse
    enforces this at parse time). Attached via ``Annotated[SomeArgs, Mutex()]``;
    pass ``Mutex(required=True)`` to require exactly one.
    """

    __slots__ = ("required",)

    def __init__(self, required: bool = False) -> None:
        self.required = required

    def __repr__(self) -> str:
        return f"Mutex(required={self.required!r})"
