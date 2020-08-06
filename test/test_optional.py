from typed_args import TypedArgs, add_argument, typed_args
from typing import Optional


def test_optional_argument():
    @typed_args
    class Args(TypedArgs):
        config: Optional[str] = add_argument('-c', '--config')

    args = Args.from_args([])

    assert args.config == None

    args = Args.from_args('-c /path'.split())

    assert args.config == '/path'


def test_optional_with_default():
    @typed_args
    class Args(TypedArgs):
        config: str = add_argument('-c', '--config', default='/path')

    args = Args.from_args([])

    assert args.config == '/path'

    args = Args.from_args('-c /other'.split())

    assert args.config == '/other'
