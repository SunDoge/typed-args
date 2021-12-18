from enum import Enum
from typing import Type, Dict


def get_members(x: Type[Enum]) -> Dict[str, Enum]:
    return getattr(x, "__members__")
