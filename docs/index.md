# Welcome to `typed-args`

## Introduction

`typed-args` is a Python package for creating command line interfaces in a type-annotated way with standard python library `argparse`. 
The program defines what arguments it requires, and `typed-args` will figure out how to parse them out of `sys.argv`.


What does it look like? Here is an [example](https://docs.python.org/3/library/argparse.html#example) from `argparse` docs and is rewritten with `typed-args`:

```python
import typed_args as ta
from typing import List, Callable


@ta.argument_parser(
    description='Process some integers.'
)
class Args:
    integers: List[int] = ta.add_argument(
        metavar='N', type=int, nargs='+',
        help='an integer for the accumulator'
    )
    accumulate: Callable[[List[int]], int] = ta.add_argument(
        '--sum',
        action='store_const',
        const=sum, default=max,
        help='sum the integers (default: find the max)'
    )


args = Args.parse_args()
print(args.accumulate(args.integers))
```

Assuming the above Python code is saved into a file called `prog.py`, it can be run at the command line and it provides useful help messages:

```text
$ python prog.py -h
usage: prog.py [-h] [--sum] N [N ...]

Process some integers.

positional arguments:
  N           an integer for the accumulator

optional arguments:
  -h, --help  show this help message and exit
  --sum       sum the integers (default: find the max)
```

When run with the appropriate arguments, it prints either the sum or the max of the command-line integers:

```text
$ python prog.py 1 2 3 4
4

$ python prog.py 1 2 3 4 --sum
10
```

If invalid arguments are passed in, an error will be displayed:

```text
$ python prog.py a b c
usage: prog.py [-h] [--sum] N [N ...]
prog.py: error: argument N: invalid int value: 'a'
```


## Installation

You can get the library directly from PyPI:

```shell
pip install typed-args
```
