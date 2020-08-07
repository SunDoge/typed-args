# TypedArgs

[![Build Status](https://travis-ci.org/SunDoge/typed-args.svg?branch=master)](https://travis-ci.org/SunDoge/typed-args)

Strong type args.

This project is inspired by [TeXitoi/structopt](https://github.com/TeXitoi/structopt).

## Install

From pypi

```bash
pip install typed-args
```

If you want to use it on python 3.5 and 3.6 please install `dataclasses`:

```bash
pip install dataclasses
```

## Usage

```python
import argparse
from dataclasses import dataclass

from typed_args import TypedArgs, add_argument


@dataclass
class Args(TypedArgs):
    data: str = add_argument(metavar='DIR', help='path to dataset')
    arch: str = add_argument('-a', '--arch', metavar='ARCH', default='resnet18',
                             help='model architecture (default: resnet18)')
    num_workers: int = add_argument('-j', '--workers', default=4, metavar='N',
                                    help='number of data loading workers (default: 4)')

    def parser_factory(self):
        return argparse.ArgumentParser('PROG')


def test_args():
    data = '/path/to/dataset'
    arch = 'resnet50'
    num_workers = 8

    argv = f'{data} -a {arch} --workers {num_workers}'.split()

    args = Args.from_args(argv)  

    assert args.arch == arch
    assert args.data == data
    assert args.num_workers == num_workers


if __name__ == "__main__":
    test_args()
```

## Limitation

Currently, we don't support `add_group` and `sub parser`.