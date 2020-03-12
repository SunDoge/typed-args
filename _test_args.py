import logging
import sys
from dataclasses import dataclass

from typed_args import TypedArgs, add_argument

logging.basicConfig(level=logging.DEBUG)


# class Args(TypedArgs):
#
#     def __init__(self):
#         parser = argparse.ArgumentParser()
#
#         self.data: ArgType[str] = parser.add_argument('data', metavar='DIR',
#                                                       help='path to dataset')
#         self.arch: ArgType[str] = parser.add_argument('-a', '--arch', metavar='ARCH', default='resnet18',
#                                                       help='model architecture: ' +
#                                                            ' (default: resnet18)')
#         self.num_workers: ArgType[int] = parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
#                                                              help='number of data loading workers (default: 4)')
#
#         self.parse_args_from(parser)

@dataclass
class Args(TypedArgs):
    data: str = add_argument(
        'data',
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


def test_args():
    data = '/path/to/dataset'
    arch = 'resnet50'
    num_workers = 8

    argv = f'{data} -a {arch} --workers {num_workers}'.split()

    sys.argv.extend(argv)

    args = Args.from_args()
    args = Args.from_known_args()

    assert args.arch == arch
    assert args.data == data
    assert args.num_workers == num_workers


if __name__ == "__main__":
    test_args()
