from enum import Enum
from typing import Type, Dict
from dataclasses import Field

def get_members(x: Type[Enum]) -> Dict[str, Enum]:
    return getattr(x, "__members__")


def get_dataclass_fields(x) -> Dict[str, Field]:
    return getattr(x, "__dataclass_fields__")
