import logging
import sys
from dataclasses import dataclass

from typed_args import TypedArgs, add_argument
import argparse

logging.basicConfig(level=logging.DEBUG)


@dataclass(repr=False)
class Args(TypedArgs):
    foo: str = 'bar'
    data: str = add_argument(
        metavar='DIR',
        help='path to dataset'
    )
    arch: str = add_argument(
        '-a', '--arch',
        metavar='ARCH',
        default='resnet18',
        help='model architecture (default: resnet18)'
    )
    num_workers: int = add_argument(
        '-j', '--workers',
        default=4,
        metavar='N',
        help='number of data loading workers (default: 4)'
    )

    def parser_factory(self):
        return argparse.ArgumentParser('PROG')


@dataclass
class Args1(Args):
    foo: str = add_argument('--foo')


def test_args():
    data = '/path/to/dataset'
    arch = 'resnet50'
    num_workers = 8

    argv = f'{data} -a {arch} --workers {num_workers}'.split()

    # sys.argv.extend(argv)

    args = Args.from_args(argv)
    # args = Args.from_known_args()
    # args = Args1.from_args(argv)

    # args = Args.from_args()
    print(args)

    # assert args.arch == arch
    # assert args.data == data
    # assert args.num_workers == num_workers


if __name__ == "__main__":
    test_args()
    # from test.test_add_argument import *
    # test_name_or_flags()
