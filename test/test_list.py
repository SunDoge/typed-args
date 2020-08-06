from typed_args import TypedArgs, add_argument, typed_args
from typing import List


def test_list():
    """
    https://docs.python.org/3/library/argparse.html#nargs
    :return:
    """

    @typed_args()
    class Args(TypedArgs):
        foo: List[str] = add_argument('--foo', nargs=2)
        bar: List[str] = add_argument(nargs=1)

    args = Args.from_args('c --foo a b'.split())

    assert args.foo == ['a', 'b']
    assert args.bar == ['c']
