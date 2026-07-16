# typed-args

[![PyPI version](https://img.shields.io/pypi/v/typed-args.svg)](https://pypi.org/project/typed-args/)
[![Python versions](https://img.shields.io/pypi/pyversions/typed-args.svg)](https://pypi.org/project/typed-args/)
[![Python package](https://github.com/SunDoge/typed-args/actions/workflows/python-package.yml/badge.svg)](https://github.com/SunDoge/typed-args/actions/workflows/python-package.yml)
[![Publish](https://github.com/SunDoge/typed-args/actions/workflows/python-publish.yml/badge.svg)](https://github.com/SunDoge/typed-args/actions/workflows/python-publish.yml)

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
    model_config = ta.ParserConfig(description="Process some integers.")
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
- **Parser config is `model_config`.** Use `ParserConfig(prog=..., description=...)`,
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

Global flags (the `common` field) work before the subcommand (argparse behavior);
after-subcommand globals are not supported.

## API

- `TypedArgs` — `pydantic.BaseModel` subclass adding `parse_args(argv=None, *, parser=None)`
  and `parse_known_args(...)` classmethods.
- `ParserConfig` — `ConfigDict` subclass with `argparse.ArgumentParser` fields.
- `Arg(*option_strings, **kwargs)` — argparse passthrough marker for a field.
- `parse(model, argv=None, *, parser=None)` / `parse_known_args(...)` — free functions
  for users who don't subclass `TypedArgs`.
- `DefaultHelpFormatter` — strips dotted dest prefixes from help output.

## Feature support

| Feature | Status | How / note |
|---|:--:|---|
| **Args** | | |
| Positional / optional | ✓ | `Arg()` / `Arg("-f", "--foo")` |
| `action` (store_true / store_const / append / count / custom) | ✓ | auto for `bool`; `Arg(action=...)` |
| `nargs` | ✓ | auto `*` for `list`; `Arg(nargs=...)` |
| `const` / `default` / `type` / `choices` / `required` / `help` / `metavar` | ✓ | `Arg(...)` passthrough |
| Custom `Action` | ✓ | via `Arg(**kwargs)` |
| `dest` override | ✗ | rejected — `dest` is the field-path link to the model |
| **Types & validation** | | |
| Type-driven structure (`bool`→flag, `Literal`→choices, `list`→nargs, required→positional) | ✓ | |
| `Field` constraints (`gt`/`le`/…), `field_validator`, `ValidationError` | ✓ | pydantic at parse time |
| **Help** | | |
| Attribute docstring → `help` | ✓ | `use_attribute_docstrings`, on by default |
| `help` precedence: `Arg(help=)` > `Field(description=)` > docstring | ✓ | |
| `DefaultHelpFormatter` (strips dotted dest) | ✓ | |
| **Parser config** | | |
| `prog` / `description` / `epilog` / `prefix_chars` / `fromfile_prefix_chars` / `argument_default` / `conflict_handler` / `add_help` / `allow_abbrev` / `exit_on_error` / `formatter_class` | ✓ | `ParserConfig` in `model_config` |
| Custom `ArgumentParser` (escape hatch) | ✓ | `parse_args(parser=...)` |
| **Subcommands** | | |
| Discriminated union + `match` dispatch | ✓ | |
| Optional subcommand (`required=False`) | ✓ | `Optional[Union[...]] = None` |
| Nested subcommands | ✓ | recursive |
| Subparsers section `title` / `description` / `prog` / `metavar` | ✓ | `Subparsers(...)` marker |
| Subcommand aliases (`add_parser(aliases=...)`) | ✗ | not implemented |
| Per-subparser config (`prog` / `description` / `formatter_class` / `help`) | ✗ | not implemented |
| **Groups** | | |
| Argument group (titled section) | ✓ | `Group(...)` marker |
| Mutually exclusive group | ✓ | `Mutex(...)` marker |
| **Composition** | | |
| Nested model as a field (library args as an attribute) | ✓ | |
| Merge into a host `argparse` parser | ✓ | `add_arguments` / `from_namespace` |
| Global args before the subcommand | ✓ | nested model on the main parser |
| Global args after the subcommand (clap `global=true`) | ✗ | cut — put globals before the subcommand |
| Prefixing a nested model's flags (`--lib-host`) | ✗ | decided against |
| **Parsing** | | |
| `parse_args` / `parse_known_args` | ✓ | |
| `parse_intermixed_args` | ✗ | not exposed |

