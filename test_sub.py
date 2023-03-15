import dataclasses
import argparse
from typed_args._parser import add_argument, add_argument_group, add_parser, add_subparsers
from typed_args._utils import SubcommandEnum
from icecream import ic
import logging
from typed_args._core import argument_parser
import functools


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


@argument_parser(prog='dddd')
@dataclasses.dataclass
class Args:
    x1: str = add_argument()
    group1: Group1 = add_argument_group()
    group2: Group2 = add_argument_group()
    sub_cmd: SubCommands = add_subparsers()


def test():
    logging.basicConfig(level=logging.DEBUG)

    args = Args.parse_args()

    ic(args)


if __name__ == '__main__':
    test()
