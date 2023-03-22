import typed_args as ta
from icecream import ic
import logging
import pickle


@ta.dataclass
class Group1:
    x2: str = ta.add_argument('--x2')
    x3: str = ta.add_argument('--x3')


@ta.dataclass
class Group2:
    x4: str = ta.add_argument('--x4')
    """
    x4 in group2
    """

    x5: str = ta.add_argument('--x5')
    """x5 in group2"""


@ta.dataclass
class Cmd1:
    x6: str = ta.add_argument('--x6')
    x7: str = ta.add_argument('--x7')


@ta.dataclass
class Cmd2:
    x6: str = ta.add_argument('--x6')
    x7: str = ta.add_argument('--x7')
    x8: str = ta.add_argument('--x8')


class SubCommands(ta.SubcommandEnum):
    CMD1: Cmd1 = ta.add_parser('cmd1')
    CMD2: Cmd2 = ta.add_parser('cmd2')


@ta.argument_parser(prog='dddd')
class Args(ta.TypedArgs):
    x1: str = ta.add_argument()
    group1: Group1 = ta.add_argument_group()
    group2: Group2 = ta.add_argument_group()
    sub_cmd: SubCommands = ta.add_subparsers()
    x9: int = ta.add_argument('--x9', type=int)


def test():
    logging.basicConfig(level=logging.DEBUG)

    args = Args.parse_args()

    ic(args)
    args.group1.x2

    pickle.dumps(args)


if __name__ == '__main__':
    test()
