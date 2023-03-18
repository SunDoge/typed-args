# typed-args

[![Github Actions](https://img.shields.io/github/actions/workflow/status/SunDoge/typed-args/python-package.yml?branch=master&style=for-the-badge)](https://github.com/SunDoge/typed-args/actions/workflows/python-package.yml)
[![Pypi](https://img.shields.io/pypi/v/typed-args?style=for-the-badge)](https://pypi.org/project/typed-args/)

Type command line argument parser for Python.

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
class Args:
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
class Args:
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


