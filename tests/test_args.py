# import argparse
# from dataclasses import dataclass

# from typed_args import TypedArgs, add_argument



# """
# argparse
# """
# parser = argparse.ArgumentParser(prog='PROG')
# parser.add_argument(
#     'data', metavar='DIR', type=str,
#     help='path to dataset'
# )
# parser.add_argument(
#     '-a', '--arch', metavar='ARCH', default='resnet18', type=str,
#     help='model architecture (default: resnet18)'
# )
# parser.add_argument(
#     '-j', '--workers', default=4, metavar='N', type=int, dest='num_workers',
#     help='number of data loading workers (default: 4)'
# )

# """
# TypedArgs
# """


# @dataclass
# class Args(TypedArgs):
#     data: str = add_argument(metavar='DIR', help='path to dataset')
#     arch: str = add_argument('-a', '--arch', metavar='ARCH', default='resnet18',
#                              help='model architecture (default: resnet18)')
#     num_workers: int = add_argument('-j', '--workers', default=4, metavar='N',
#                                     help='number of data loading workers (default: 4)')

#     def parser_factory(self):
#         return argparse.ArgumentParser('PROG')


# def test_args():
#     data = '/path/to/dataset'
#     arch = 'resnet50'
#     num_workers = 8

#     argv = f'{data} -a {arch} --workers {num_workers}'.split()

#     """
#     from_args = parse_args, from_known_args = parse_known_args
#     """
#     typed_args = Args.from_args(argv)
#     args = parser.parse_args(argv)

#     assert args.arch == typed_args.arch
#     assert args.data == typed_args.data
#     assert args.num_workers == typed_args.num_workers


# if __name__ == "__main__":
#     test_args()
