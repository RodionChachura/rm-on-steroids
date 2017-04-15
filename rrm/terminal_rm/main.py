import os

from ..config import config
from ..config.config import JSONConfig
from ..core.trash import Trash
from ..core import utils

from schedule import setup_clear_schedule
from logger import setup_logger
from parser import get_tooled_parser
from talking_trash import TalkingTrash


def main():
    parser = get_tooled_parser()
    args = parser.parse_args()
    if args.with_config:
        configs = JSONConfig(args.with_config, write=False)
    else:
        configs = JSONConfig()
    setup_logger(config.LOG_LOCATION, configs.level_for_log_in_file, configs.level_for_log_in_terminal)
    setup_clear_schedule(configs.clear_each)
    trash_location = os.path.join(configs.trash_location, config.TRASH_NAME)
    trash = Trash(trash_location, configs.trash_size)
    t = TalkingTrash(trash, configs)

    if args.silent:
        utils.make_silent()
    if args.dry:
        trash.dry = True
    if args.move:
        path = args.move
        if args.rf:
            return t.complete_remove(path)
        return t.move(path)
    if args.move_by_regex:
        regex = args.move_by_regex
        if args.rf:
            return t.complete_remove_by_regex(regex)
        return t.move_by_regex(regex)
    if args.remove:
        i = args.remove
        return t.remove(i)
    if args.restore:
        i = args.restore
        return t.restore(i)
    if args.ls:
        if args.size:
            return t.trash_size_info()
        if args.only:
            return t.trash_only(args.only)
        return t.get_all_with_shortest_ids()
    if args.clear:
        return t.clear()

    print 'rm on steroids'
