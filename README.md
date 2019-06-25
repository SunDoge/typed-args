# TypeArgs

Strong type args.

## Install

```bash
pip install git+https://github.com/SunDoge/typeargs.git
```

## Usage

```python
from typeargs import TypeArgs
from dataclasses import dataclass
import argparse
import sys


parser = argparse.ArgumentParser()
@dataclass
class Args(TypeArgs):
    data: str = parser.add_argument('data', metavar='DIR',
                                    help='path to dataset')
    arch: str = parser.add_argument('-a', '--arch', metavar='ARCH', default='resnet18',
                                    help='model architecture: ' +
                                    ' (default: resnet18)')
    num_workers: int = parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
                                           help='number of data loading workers (default: 4)')


if __name__ == "__main__":
    data = '/path/to/dataset'
    arch = 'resnet50'
    num_workers = 8

    argv = f'{data} -a {arch} --workers {num_workers}'.split()

    sys.argv.extend(argv)

    args = Args(parser.parse_args())

    assert args.arch == arch
    assert args.data == data
    assert args.num_workers == num_workers
```
