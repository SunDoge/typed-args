# Welcome to `typed-args`

## Introduction

`typed-args` is a typed command-line argument parser for Python, inspired by Rust's [clap](https://docs.rs/clap).
You define a `pydantic` model — its types drive the CLI, and parsing runs real runtime validation.
Subcommands are discriminated unions you dispatch with `match`.

Requires Python 3.10+ and `pydantic` 2.

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

$ python prog.py -h
usage: prog.py [-h] [-w WORKERS] N [N ...]

Process some integers.

positional arguments:
  N                     an integer for the accumulator

options:
  -h, --help            show this help message and exit
  -w WORKERS, --workers WORKERS
                        worker count
```

The `Field(gt=0, le=32)` constraint is enforced at parse time — `workers=99`
raises a `pydantic.ValidationError` instead of silently producing a bad value.

## Installation

```shell
pip install typed-args
```
