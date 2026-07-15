# typed-args

A typed command-line argument parser for Python, inspired by Rust's [clap](https://docs.rs/clap).
Define a `pydantic` model — its types drive the CLI, and parsing runs real runtime
validation. Subcommands are discriminated unions you dispatch with `match`.

Requires Python 3.10+ and `pydantic` 2.

## Installation

```bash
pip install typed-args
```

## A first example

```python
from typing import Annotated, List

import typed_args as ta
from pydantic import Field


class Args(ta.TypedArgs):
    model_config = ta.TypedArgsConfig(description="Process some integers.")
    integers: Annotated[List[int], ta.Arg(metavar="N", nargs="+", help="an integer for the accumulator")]
    workers: Annotated[int, Field(gt=0, le=32), ta.Arg("-w", "--workers", help="worker count")] = 4


args = Args.parse_args()
print(args.integers, "max =", max(args.integers), "workers =", args.workers)
```

```text
$ python prog.py 1 2 3 4 -w 8
[1, 2, 3, 4] max = 4 workers = 8

$ python prog.py 1 -w 99
workers
  Input should be less than or equal to 32 ...
```

The `Field(gt=0, le=32)` constraint is enforced at parse time — `workers=99`
raises a `pydantic.ValidationError` instead of silently producing a bad value.

## How it works

- **Types drive structure.** `bool` → `--flag` (store_true), `Literal[...]` → `choices`,
  `list` → `nargs`, `Optional`/defaults → optional args, required scalars → positionals.
- **`Arg(...)` is the argparse passthrough.** Attach it via `Annotated[T, Arg(...)]` for
  option strings, `help`, `metavar`, `action`, `nargs`, `const`, ... It overlays
  argparse params on top of the type-derived defaults.
- **Docstrings become `help` automatically.** A bare string literal on the line after a
  field is used as its `help` text (via pydantic's `use_attribute_docstrings`, on by
  default). Precedence: `Arg(help=...)` > `Field(description=...)` > attribute docstring.
- **Validation is real.** `pydantic` coerces and validates the parsed namespace, so
  `Field(...)`, `field_validator`, and structured error messages all work.
- **Parser config is `model_config`.** Use `TypedArgsConfig(prog=..., description=...)`,
  which subclasses pydantic's `ConfigDict` and mixes freely with pydantic config
  (`frozen`, `str_strip_whitespace`, ...). For full control, pass your own
  `argparse.ArgumentParser` via `Args.parse_args(parser=...)`.

## Subcommands

Subcommands are a pydantic discriminated union; dispatch with `match`:

```python
from typing import Annotated, Literal, Union

import typed_args as ta
from pydantic import Field


class GlobalArgs(ta.TypedArgs):
    verbose: Annotated[bool, ta.Arg("-v", "--verbose")] = False


class AddArgs(ta.TypedArgs):
    cmd: Literal["add"] = "add"
    file: Annotated[str, ta.Arg(help="file to add")]
    force: Annotated[bool, ta.Arg("--force")] = False


class RemoveArgs(ta.TypedArgs):
    cmd: Literal["remove"] = "remove"
    file: Annotated[str, ta.Arg(help="file to remove")]
    recursive: Annotated[bool, ta.Arg("-r", "--recursive")] = False


class Root(ta.TypedArgs):
    common: GlobalArgs
    subcommand: Annotated[Union[AddArgs, RemoveArgs], Field(discriminator="cmd")]


root = Root.parse_args()
match root.subcommand:
    case AddArgs(file=f, force=True):
        print("force-add", f)
    case AddArgs(file=f):
        print("add", f)
    case RemoveArgs(file=f, recursive=True):
        print("recursive remove", f)
    case RemoveArgs(file=f):
        print("remove", f)
```

Global flags (the `common` field) work both before and after the subcommand.

## API

- `TypedArgs` — `pydantic.BaseModel` subclass adding `parse_args(argv=None, *, parser=None)`
  and `parse_known_args(...)` classmethods.
- `TypedArgsConfig` — `ConfigDict` subclass with `argparse.ArgumentParser` fields.
- `Arg(*option_strings, **kwargs)` — argparse passthrough marker for a field.
- `parse(model, argv=None, *, parser=None)` / `parse_known_args(...)` — free functions
  for users who don't subclass `TypedArgs`.
- `DefaultHelpFormatter` — strips dotted dest prefixes from help output.
