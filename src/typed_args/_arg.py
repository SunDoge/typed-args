from __future__ import annotations

import argparse
from typing import Any, Callable, Iterable

__all__ = ["Arg"]


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
        dest: str | None = None,
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
            "dest": dest,
        }.items():
            if v is not None:
                kwargs[k] = v
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return f"Arg({self.option_strings!r}, {self.kwargs!r})"
