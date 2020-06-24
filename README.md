# TypedArgs

[![Build Status](https://travis-ci.org/SunDoge/typed-args.svg?branch=master)](https://travis-ci.org/SunDoge/typed-args)

Strong type args.

This project is inspired by [TeXitoi/structopt](https://github.com/TeXitoi/structopt).

## Install

From pypi

```bash
pip install typed-args
```

From github
```bash
pip install git+https://github.com/SunDoge/typed-args.git@v0.3
```

If you want to use it on python 3.5 and 3.6 please install `dataclasses`:

```bash
pip install dataclasses
```

## Usage

```python
from dataclasses import dataclass

from typed_args import TypedArgs, add_argument


@dataclass
class Args(TypedArgs):
    data: str = add_argument(metavar='DIR', help='path to dataset')
    arch: str = add_argument('-a', '--arch', metavar='ARCH', default='resnet18',
                             help='model architecture (default: resnet18)')
    num_workers: int = add_argument('-j', '--workers', default=4, metavar='N',
                                    help='number of data loading workers (default: 4)')

    def __post_init__(self):
        """
        anothor way to init
        """
        self._parse_args()


def test_args():
    data = '/path/to/dataset'
    arch = 'resnet50'
    num_workers = 8

    argv = f'{data} -a {arch} --workers {num_workers}'.split()

    args = Args.from_args(argv)

    args1 = Args() # if __post_init__ is defined

    assert args.arch == arch
    assert args.data == data
    assert args.num_workers == num_workers


if __name__ == "__main__":
    test_args()
```

## Limitation

Currently, we don't support add_group and sub parser.