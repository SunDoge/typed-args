import argparse
from dataclasses import dataclass

__version__ = '0.1.0'


@dataclass
class TypeArgs:
    args: argparse.Namespace

    def __post_init__(self):

        for key, value in self.__dict__.items():
            if isinstance(value, argparse.Action):
                dest = value.dest
                self.__dict__[key] = self.args.__dict__[dest]
