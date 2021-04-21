import sys

if sys.version_info.major == 3 and sys.version_info.minor <= 6:
    import warnings

    warnings.warn(
        'Please `pip install dataclasses` if you are using python 3.6 and below'
    )

from ._typed_args import TypedArgs, add_argument

__version__ = "0.5.0.a2"
