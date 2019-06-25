import argparse
from dataclasses import dataclass

__version__ = '0.1.0'


@dataclass
class TypeArgs:
    parser: argparse.ArgumentParser
    parse_known_args: bool = False

    def __post_init__(self):

        if self.parse_known_args:
            args, _ = self.parser.parse_known_args()
        else:
            args = self.parser.parse_args()

        for key, value in self.__dict__.items():
            if isinstance(value, argparse.Action):
                dest = value.dest
                self.__dict__[key] = args.__dict__[dest]
