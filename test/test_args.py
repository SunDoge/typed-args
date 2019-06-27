import argparse
import sys

from typeargs import TypeArgs


class Args(TypeArgs):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.data: str = self.parser.add_argument('data', metavar='DIR',
                                                  help='path to dataset')
        self.arch: str = self.parser.add_argument('-a', '--arch', metavar='ARCH', default='resnet18',
                                                  help='model architecture: ' +
                                                  ' (default: resnet18)')
        self.num_workers: int = self.parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
                                                         help='number of data loading workers (default: 4)')

        self.parse_args()


def test_args():
    data = '/path/to/dataset'
    arch = 'resnet50'
    num_workers = 8

    argv = f'{data} -a {arch} --workers {num_workers}'.split()

    sys.argv.extend(argv)

    args = Args()

    assert args.arch == arch
    assert args.data == data
    assert args.num_workers == num_workers
