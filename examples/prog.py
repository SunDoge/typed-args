"""Minimal example: typed args with validation."""

from typing import Annotated, List

import typed_args as ta
from pydantic import Field


class Args(ta.TypedArgs):
    model_config = ta.ParserConfig(description="Process some integers.")
    integers: Annotated[
        List[int], ta.Arg(metavar="N", nargs="+", help="an integer for the accumulator")
    ]
    workers: Annotated[
        int, Field(gt=0, le=32), ta.Arg("-w", "--workers", help="worker count")
    ] = 4


args = Args.parse_args()
print(args.integers, "max =", max(args.integers), "workers =", args.workers)
