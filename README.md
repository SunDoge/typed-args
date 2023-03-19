# typed-args

[![Github Actions](https://img.shields.io/github/actions/workflow/status/SunDoge/typed-args/python-package.yml?branch=master&style=for-the-badge)](https://github.com/SunDoge/typed-args/actions/workflows/python-package.yml)
[![Pypi](https://img.shields.io/pypi/v/typed-args?style=for-the-badge)](https://pypi.org/project/typed-args/)

This project is inspired by [TeXitoi/structopt](https://github.com/TeXitoi/structopt).

## Introduction

`typed-args` is a Python package for creating command line interfaces with type annotations. 
The program defines what arguments it requires, and `typed-args` will figure out how to parse them out of `sys.argv`. 
`typed-args` use standard python library `argparse` and `dataclasses` so no need to install any dependencies after Python 3.6. 
Its API is very similar to `argparse`. 


What does it look like? Here is an [example](https://docs.python.org/3/library/argparse.html#example) from `argparse` docs and is rewritten with `typed-args`:

```python
import typed_args as ta
from typing import List, Callable


@ta.argument_parser(
    description='Process some integers.'
)
class Args(ta.TypedArgs):
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

From pypi

```bash
pip install typed-args
```

If you want to use it on python 3.5 and 3.6 please install `dataclasses`:

```bash
pip install dataclasses
```

## Core Functionality

Check [_test_v0_6.py](https://github.com/SunDoge/typed-args/blob/master/_test_v0_6.py) for `add_argument_group` and `add_subparsers`.


### Create a parser

`argparse`

```python
import argparse
parser = argparse.ArgumentParser(prog='ProgramName')
```

`typed-args`

```python
import typed_args as ta

@ta.argument_parser(prog='ProgramName')
class Args(ta.TypedArgs):
    pass
```

### Add arguments

`argparse`

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('filename')           # positional argument
parser.add_argument('-c', '--count')      # option that takes a value
parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag
```

`typed-args`

```python
import typed_args as ta

@ta.argument_parser()
class Args(ta.TypedArgs):
    filename: str = ta.add_argument()                    # positional argument, use the attribute name automatically
    count: str = ta.add_argument('-c', '--count')        # option that takes a value, also can be annotated as Optional[str]
    verbose: bool = ta.add_argument('-v', '--verbose', 
                                    action='store_true') # on/off flag
```

### Parse args

`argparse`

```python
args = parser.parse_args()
print(args.filename, args.count, args.verbose)
```

`typed-args`

```python
args = Args.parse_args()
print(args.filename, args.count, args.verbose)
```


