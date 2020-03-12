# TypedArgs

[![Build Status](https://travis-ci.org/SunDoge/typed-args.svg?branch=master)](https://travis-ci.org/SunDoge/typed-args)

Strong type args.

## Install

From pypi

```bash
pip install typed-args
```

From github
```bash
pip install git+https://github.com/SunDoge/typed-args.git@v0.3
```

## Usage

```python
from dataclasses import dataclass

from typed_args import TypedArgs, add_argument


@dataclass
class Args(TypedArgs):
    data: str = add_argument('data', metavar='DIR', help='path to dataset')
    arch: str = add_argument('-a', '--arch', metavar='ARCH', default='resnet18',
                             help='model architecture (default: resnet18)')
    num_workers: int = add_argument('-j', '--workers', default=4, metavar='N',
                                    help='number of data loading workers (default: 4)')


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
