import argparse

__version__ = '0.2.0'


class TypeArgs:
    parser: argparse.ArgumentParser
    _args: argparse.Namespace

    def parse_args(self):
        self._args = self.parser.parse_args()
        self._assign_args()

    def parse_known_args(self):
        self._args, _ = self.parser.parse_known_args()
        self._assign_args()

    def _assign_args(self):

        for key, value in self.__dict__.items():
            if isinstance(value, argparse.Action):
                dest = value.dest
                self.__dict__[key] = self._args.__dict__[dest]
