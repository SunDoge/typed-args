# from typed_args import TypedArgs, add_argument, dataclass
import typed_args as tp
import pickle
from typing import Optional
from dataclasses import dataclass


@dataclass()
class Args(tp.TypedArgs):
    foo: Optional[str] = tp.add_argument('--foo')


def test_pickle():
    args = Args.from_args([])
    _pickled_args = pickle.dumps(args)
    assert _pickled_args


if __name__ == "__main__":
    test_pickle()
