import logging
import pickle
from dataclasses import dataclass
from typing import Optional

import typed_args._typed_args as tp

_logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.INFO)


_logger.debug('this is debug')


@dataclass
class Args2(tp.TypedArgs):
    batch_size: str = tp.add_argument('--batch-size', type=int)


@dataclass
class Args1(tp.TypedArgs):
    foo: str = tp.add_argument()
    bar: str = tp.add_argument('--bar')
    sub: Args2 = Args2()

# rich.print(A.__annotations__)
# rich.print(A.__dataclass_fields__)


args1 = Args1.from_args()
print(args1.foo)

s = pickle.dumps(args1)
