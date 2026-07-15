from typing import Annotated

import pytest
from pydantic import Field, ValidationError, field_validator

import typed_args as ta


def test_numeric_range_rejects_out_of_bounds():
    class Args(ta.TypedArgs):
        count: Annotated[int, Field(gt=0, le=10), ta.Arg("-n")] = 5

    with pytest.raises(ValidationError):
        Args.parse_args(["-n", "99"])


def test_numeric_range_accepts_in_bounds():
    class Args(ta.TypedArgs):
        count: Annotated[int, Field(gt=0, le=10), ta.Arg("-n")] = 5

    assert Args.parse_args(["-n", "7"]).count == 7


def test_field_validator_runs():
    class Args(ta.TypedArgs):
        name: Annotated[str, ta.Arg("--name")] = "x"

        @field_validator("name")
        @classmethod
        def upper(cls, v: str) -> str:
            return v.upper()

    assert Args.parse_args(["--name", "abc"]).name == "ABC"


def test_wrong_type_rejected():
    class Args(ta.TypedArgs):
        n: Annotated[int, ta.Arg("-n")] = 0

    with pytest.raises(Exception):
        Args.parse_args(["-n", "notanint"])
