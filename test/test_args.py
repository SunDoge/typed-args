from dataclasses import dataclass

from typed_args import TypedArgs, add_argument


@dataclass
class Args(TypedArgs):
    data: str = add_argument(metavar='DIR', help='path to dataset')
    arch: str = add_argument('-a', '--arch', metavar='ARCH', default='resnet18',
                             help='model architecture (default: resnet18)')
    num_workers: int = add_argument('-j', '--workers', default=4, metavar='N',
                                    help='number of data loading workers (default: 4)')


def test_args():
    data = '/path/to/dataset'
    arch = 'resnet50'
    num_workers = 8

    argv = f'{data} -a {arch} --workers {num_workers}'.split()

    # sys.argv.extend(argv)

    args = Args.from_known_args(argv)

    assert args.arch == arch
    assert args.data == data
    assert args.num_workers == num_workers


def test_known_args():
    data = '/path/to/dataset'
    arch = 'resnet50'
    num_workers = 8

    argv = f'{data} -a {arch} --workers {num_workers}'.split()

    # sys.argv.extend(argv)

    args = Args.from_args(argv)

    assert args.arch == arch
    assert args.data == data
    assert args.num_workers == num_workers


if __name__ == "__main__":
    # test_args()
    test_known_args()
