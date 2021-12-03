try:
    from dataclasses import dataclass
except ImportError as e:
    import warnings
    warnings.warn(
        'Please `pip install dataclasses` if you are using Python 3.5 or 3.6'
    )
    raise e

from ._typed_args import TypedArgs, add_argument

__version__ = "0.5.2"

__all__ = [
    'TypedArgs', 'add_argument'
]
