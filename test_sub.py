import dataclasses
import argparse
from typed_args._parser import add_argument, add_argument_group, add_parser, add_subparsers, _parse_dataclass
from typed_args._assigner import _assign_dataclass
from typed_args._utils import SubcommandEnum
from icecream import ic
import logging


@dataclasses.dataclass
class Group1:
    x2: str = add_argument('--x2')
    x3: str = add_argument('--x3')


@dataclasses.dataclass
class Group2:
    x4: str = add_argument('--x4')
    x5: str = add_argument('--x5')


@dataclasses.dataclass
class Cmd1:
    x6: str = add_argument('--x6')
    x7: str = add_argument('--x7')


@dataclasses.dataclass
class Cmd2:
    x6: str = add_argument('--x6')
    x7: str = add_argument('--x7')
    x8: str = add_argument('--x8')


class SubCommands(SubcommandEnum):
    CMD1: Cmd1 = add_parser('cmd1')
    CMD2: Cmd2 = add_parser('cmd2')


@dataclasses.dataclass
class Args:
    x1: str = add_argument('--x1')
    group1: Group1 = add_argument_group()
    group2: Group2 = add_argument_group()
    sub_cmd: SubCommands = add_subparsers()


def test():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    _parse_dataclass(parser, Args)
    # ic(parser.print_help())

    ns = parser.parse_args()
    ic(ns)
    ic(Args())
    args = Args()
    ic(SubCommands.CMD1(10000) == SubCommands.CMD1)
    ic(SubCommands.CMD1)
    ic(id(SubCommands.CMD1))
    ic(SubCommands.CMD1 == SubCommands.CMD1(10000))

    _assign_dataclass(args, ns)
    ic(args)


if __name__ == '__main__':
    test()
