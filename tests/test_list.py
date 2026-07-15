from typing import Annotated, List

import typed_args as ta


def test_list_default_nargs_star():
    class Args(ta.TypedArgs):
        ns: Annotated[List[int], ta.Arg("-n")]

    assert Args.parse_args(["-n", "1", "2", "3"]).ns == [1, 2, 3]


def test_list_with_default_empty():
    class Args(ta.TypedArgs):
        ns: Annotated[List[int], ta.Arg("-n")] = []

    assert Args.parse_args([]).ns == []
    assert Args.parse_args(["-n", "4", "5"]).ns == [4, 5]


def test_append_action():
    class Args(ta.TypedArgs):
        item: Annotated[List[str], ta.Arg("-i", action="append")] = []

    a = Args.parse_args(["-i", "a", "-i", "b"])
    assert a.item == ["a", "b"]


def test_list_positional():
    class Args(ta.TypedArgs):
        files: Annotated[List[str], ta.Arg()]

    assert Args.parse_args(["a", "b", "c"]).files == ["a", "b", "c"]
