import argparse

__version__ = '0.1.0'


class TypedArgs:
    _parser: argparse.ArgumentParser
    _args: argparse.Namespace

    def parse_args_from(self, parser: argparse.ArgumentParser):
        self._parser = parser
        self._args = self._parser.parse_args()
        self._assign_args()

    def parse_known_args_from(self, parser: argparse.ArgumentParser):
        self._parser = parser
        self._args, _ = self._parser.parse_known_args()
        self._assign_args()

    def _assign_args(self):

        for key, value in self.__dict__.items():
            if isinstance(value, argparse.Action):
                dest = value.dest
                self.__dict__[key] = self._args.__dict__[dest]

    def __contains__(self, key):
        '''
        Copy from argparse.Namespace
        '''
        return key in self.__dict__
