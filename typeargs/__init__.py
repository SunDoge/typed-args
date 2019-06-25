import argparse
from dataclasses import dataclass

__version__ = '0.1.0'


@dataclass
class TypeArgs:
    _args: argparse.Namespace

    def __post_init__(self):

        for key, value in self.__dict__.items():
            if isinstance(value, argparse.Action):
                dest = value.dest
                self.__dict__[key] = self._args.__dict__[dest]
