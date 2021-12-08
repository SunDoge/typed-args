from dataclasses import dataclass
from typing import List

import typed_args as ta
from typed_args import TypedArgs, add_argument


def test_list():
    """
    https://docs.python.org/3/library/argparse.html#nargs
    :return:
    """

    @dataclass()
    class Args(TypedArgs):
        foo: List[str] = add_argument('--foo', nargs=2, type=str)
        bar: List[str] = add_argument(nargs=1, type=str)

    args = Args.from_args('c --foo a b'.split())

    assert args.foo == ['a', 'b']
    assert args.bar == ['c']


def test_default_list():
    @dataclass
    class Args(ta.TypedArgs):
        foo: int = ta.add_argument('--foo', type=int, default=42)
        bar: List[int] = ta.add_argument(nargs='*', default=[1, 2, 3])
        config: List[str] = ta.add_argument(
            '--config', default=[], type=str, action='append')

    args = Args.from_args([])

    assert args.bar == [1, 2, 3]
    assert args.config == []

    args1 = Args()
    assert args1.foo == 42
    assert args1.bar == [1, 2, 3]
    assert args1.config == []
