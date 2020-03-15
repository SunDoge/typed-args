from typed_args import TypedArgs, add_argument
from dataclasses import dataclass, field
from typing import *


def test_name_or_flags():
    """
    https://docs.python.org/3/library/argparse.html#name-or-flags

    :return:
    """
    import argparse
    @dataclass
    class Args(TypedArgs):
        parser: argparse.ArgumentParser = field(default_factory=lambda: argparse.ArgumentParser(prog='PROG'))
        foo: Optional[str] = add_argument('-f', '--foo')
        bar: str = add_argument()

    args = Args.from_args(['BAR'])

    assert args.bar == 'BAR'
    assert args.foo == None

    args = Args.from_args(['BAR', '--foo', 'FOO'])

    assert args.bar == 'BAR'
    assert args.foo == 'FOO'


