import argparse
from ..config import config

def get_tooled_parser():
    parser = argparse.ArgumentParser(description='rm on steroids')
    parser.add_argument('-move', type=str,
                        metavar='path', help='file or directory for moving in trash')
    parser.add_argument('-move_by_regex', type=str,
                        metavar='regex', help='moving files by regex')
    parser.add_argument('-remove', type=str,
                        metavar='id', help='remove from trash by id')
    parser.add_argument('-restore', type=str,
                        metavar='id', help='restore from trash by id')
    parser.add_argument('-clear', action='store_const', const=True, help='clear the trash')
    parser.add_argument('-ls', action='store_const', const=True, help='show trash content')

    parser.add_argument('--size', action='store_const', const=True, help='information about trash size')
    parser.add_argument('--only', type=int, help='show number of entries')

    parser.add_argument('--rf', action='store_const', const=True, help='complete remove')
    parser.add_argument('--dry', action='store_const', const=True, help='dry run of the command')
    parser.add_argument('--silent', action='store_const', const=True, help='silent run of the command')
    parser.add_argument('--with_config', type=str,
                        metavar='file', help='config for special launch')

    parser.add_argument('--on_collision', type=str, choices=config.RESTORE_COLLISION_CHOICES,
                        help='additional argument for restore command')

    return parser
