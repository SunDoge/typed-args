# TypedArgs

[![Build Status](https://travis-ci.org/SunDoge/typed-args.svg?branch=master)](https://travis-ci.org/SunDoge/typed-args)
[![Version](https://img.shields.io/pypi/v/typed-args)](https://pypi.org/project/typed-args/)

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


@dataclass
class Args(ta.TypedArgs):
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
    typed_args = Args.from_args(argv)
    args = parser.parse_args(argv)

    assert args.arch == typed_args.arch
    assert args.data == typed_args.data
    assert args.num_workers == typed_args.num_workers


if __name__ == "__main__":
    test_args()
```

## Limitation

Currently, we don't support `add_group` and `sub parser`, but we will.