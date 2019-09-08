from argparse import ArgumentParser, Action, Namespace
from typing import Union, TypeVar

__version__ = '0.2.0'


class TypedArgs:
    _parser: ArgumentParser
    _args: Namespace

    def parse_args_from(self, parser: ArgumentParser):
        self._parser = parser
        self._args = self._parser.parse_args()
        self._assign_args()

    def parse_known_args_from(self, parser: ArgumentParser):
        self._parser = parser
        self._args, _ = self._parser.parse_known_args()
        self._assign_args()

    def _assign_args(self):

        for key, value in self.__dict__.items():
            if isinstance(value, Action):
                # Get arg name from Action
                dest = value.dest
                self.__dict__[key] = self._args.__dict__[dest]

    def __contains__(self, key):
        """
        Copy from Namespace
        """
        return key in self.__dict__


"""
This type alias is added to fool PyCharm.
"""
T = TypeVar('T')
ArgType = Union[Action, T]
