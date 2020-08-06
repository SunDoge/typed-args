from typed_args import TypedArgs, add_argument, typed_args
from typing import *
import argparse


def test_name_or_flags():
    """
    https://docs.python.org/3/library/argparse.html#name-or-flags

    :return:
    """

    @typed_args(parser_factory=lambda : argparse.ArgumentParser(prog='PROG'))
    class Args(TypedArgs):
        foo: Optional[str] = add_argument('-f', '--foo')
        bar: str = add_argument()

    args = Args.from_args(['BAR'])

    assert args.bar == 'BAR'
    assert args.foo == None

    args = Args.from_args(['BAR', '--foo', 'FOO'])

    assert args.bar == 'BAR'
    assert args.foo == 'FOO'


def test_action_store():
    @typed_args
    class Args1(TypedArgs):
        foo: Optional[str] = add_argument('--foo')

    args1 = Args1.from_args('--foo 1'.split())
    assert args1.foo == '1'


def test_action_score_const():
    @typed_args
    class Args2(TypedArgs):
        foo: int = add_argument('--foo', action='store_const', const=42)

    args2 = Args2.from_args(['--foo'])
    assert args2.foo == 42


def test_action_store_true_false():
    @typed_args
    class Args3(TypedArgs):
        foo: bool = add_argument('--foo', action='store_true')
        bar: bool = add_argument('--bar', action='store_false')
        baz: bool = add_argument('--baz', action='store_false')

    args3 = Args3.from_args('--foo --bar'.split())
    assert args3.foo == True
    assert args3.bar == False
    assert args3.baz == True


def test_action_append():
    @typed_args
    class Args4(TypedArgs):
        foo: List[str] = add_argument('--foo', action='append')

    args4 = Args4.from_args('--foo 1 --foo 2'.split())
    assert args4.foo == ['1', '2']


def test_action_append_const():
    @typed_args
    class Args5(TypedArgs):
        types: List[Union[str, int]] = (
            add_argument('--str', action='append_const', const=str),
            add_argument('--int', action='append_const', const=int)
        )

    args5 = Args5.from_args('--str --int'.split())
    assert args5.types == [str, int]


def test_action_count():
    @typed_args
    class Args(TypedArgs):
        verbose: int = add_argument(
            '--verbose', '-v', action='count', default=0)

    args = Args.from_args(['-vvv'])
    assert args.verbose == 3


# TODO help, version, extend

def test_nargs_n():
    @typed_args
    class Args(TypedArgs):
        foo: List[str] = add_argument('--foo', nargs=2)
        bar: List[str] = add_argument(nargs=1)

    args = Args.from_args('c --foo a b'.split())
    assert args.bar == ['c']
    assert args.foo == ['a', 'b']


def test_nargs_optional():
    @typed_args
    class Args(TypedArgs):
        foo: str = add_argument('--foo', nargs='?', const='c', default='d')
        bar: str = add_argument(nargs='?', default='d')

    args = Args.from_args(['XX', '--foo', 'YY'])
    assert args.foo == 'YY'
    assert args.bar == 'XX'

    args = Args.from_args(['XX', '--foo'])
    assert args.foo == 'c'
    assert args.bar == 'XX'

    args = Args.from_args([])
    assert args.foo == 'd'
    assert args.bar == 'd'


def test_nargs_optional_input_and_output_files():
    pass


def test_nargs_zero_or_more():
    @typed_args
    class Args(TypedArgs):
        foo: List[str] = add_argument('--foo', nargs='*')
        bar: List[str] = add_argument('--bar', nargs='*')
        baz: List[str] = add_argument(nargs='*')

    args = Args.from_args('a b --foo x y --bar 1 2'.split())

    assert args.bar == ['1', '2']
    assert args.baz == ['a', 'b']
    assert args.foo == ['x', 'y']


def test_nargs_one_or_more():
    @typed_args
    class Args(TypedArgs):
        foo: List[str] = add_argument(nargs='+')

    args = Args.from_args(['a', 'b'])
    assert args.foo == ['a', 'b']


def test_nargs_remainder():
    @typed_args
    class Args(TypedArgs):
        foo: str = add_argument('--foo')
        command: str = add_argument()
        args: List[str] = add_argument(nargs=argparse.REMAINDER)

    args = Args.from_args('--foo B cmd --arg1 XX ZZ'.split())
    assert args.foo == 'B'
    assert args.command == 'cmd'
    assert args.args == ['--arg1', 'XX', 'ZZ']


def test_default():
    """
    TODO
    """
    pass
