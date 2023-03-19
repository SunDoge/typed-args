import typed_args as ta
from typing import List, Callable


@ta.argument_parser(
    description='Process some integers.'
)
class Args(ta.TypedArgs):
    integers: List[int] = ta.add_argument(
        metavar='N', type=int, nargs='+',
        help='an integer for the accumulator'
    )
    accumulate: Callable[[List[int]], int] = ta.add_argument(
        '--sum',
        action='store_const',
        const=sum, default=max,
        help='sum the integers (default: find the max)'
    )


args = Args.parse_args()
print(args.accumulate(args.integers))
