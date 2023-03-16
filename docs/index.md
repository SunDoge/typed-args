# Welcome to typed-args

## Introduction

`typed-args` is a Python package for creating command line interface in a strong typed way with standard python library `argparse`. 

What does it look like? Here is an example of a simple `typed-args` program:

```python
import typed_args as ta

@ta.argument_parser()
class Args:
    pass
```


## Installation

You can get the library directly from PyPI:

```shell
pip install typed-args
```
