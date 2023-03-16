import argparse

import typed_args as ta

"""
argparse
"""
parser = argparse.ArgumentParser()
parser.add_argument(
    'data', metavar='DIR', type=str,
    help='path to dataset'
)
parser.add_argument(
    '-a', '--arch', metavar='ARCH', default='resnet18', type=str,
    help='model architecture (default: resnet18)'
)
parser.add_argument(
    '-j', '--workers', default=4, metavar='N', type=int, dest='num_workers',
    help='number of data loading workers (default: 4)'
)

"""
TypedArgs
"""
@ta.argument_parser()
class Args:
    data: str = ta.add_argument(
        metavar='DIR', type=str, help='path to dataset'
    )
    arch: str = ta.add_argument(
        '-a', '--arch', metavar='ARCH', default='resnet18', type=str,
        help='model architecture (default: resnet18)'
    )
    num_workers: int = ta.add_argument(
        '-j', '--workers', default=4, metavar='N', type=int,
        help='number of data loading workers (default: 4)'
    )


def test_args():
    data = '/path/to/dataset'
    arch = 'resnet50'
    num_workers = 8

    argv = f'{data} -a {arch} --workers {num_workers}'.split()

    """
    from_args = parse_args, from_known_args = parse_known_args
    """
    typed_args = Args.parse_args(argv)
    args = parser.parse_args(argv)

    assert args.arch == typed_args.arch
    assert args.data == typed_args.data
    assert args.num_workers == typed_args.num_workers


if __name__ == "__main__":
    test_args()
