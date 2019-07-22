# TypedArgs

[![Build Status](https://travis-ci.org/SunDoge/typeargs.svg?branch=master)](https://travis-ci.org/SunDoge/typeargs)

Strong type args.

## Install

```bash
pip install git+https://github.com/SunDoge/typeargs.git
```

## Usage

```python
import argparse
import sys

from typedargs import TypedArgs


class Args(TypedArgs):

    def __init__(self):
        parser = argparse.ArgumentParser()

        self.data: str = parser.add_argument('data', metavar='DIR',
                                             help='path to dataset')
        self.arch: str = parser.add_argument('-a', '--arch', metavar='ARCH', default='resnet18',
                                             help='model architecture: ' +
                                             ' (default: resnet18)')
        self.num_workers: int = parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
                                                    help='number of data loading workers (default: 4)')

        self.parse_args_from(parser)


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


if __name__ == "__main__":
    test_args()

```
