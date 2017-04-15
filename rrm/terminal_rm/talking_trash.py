import sys
import logging

import printer
from ..core import utils
from ..core.error import TrashError
from ..config import config

logger = logging.getLogger(__name__)


def with_trash_try(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TrashError as e:
            logger.error(e.message)
            sys.exit(1)
        except Exception as e:
            logging.exception('error occured in {0} function: {1}'.format(func.__name__, e))
            sys.exit(2)
    return wrapper


class TalkingTrashMetaclass(type):
    def __new__(cls, name, bases, local):
        for attr in local:
            value = local[attr]
            if callable(value):
                local[attr] = with_trash_try(value)
        return type.__new__(cls, name, bases, local)


class TalkingTrash(object):

    __metaclass__ = TalkingTrashMetaclass

    def __init__(self, trash, configs):
        self.trash = trash
        self.configs = configs

    def size_checker(self, found):
        if isinstance(found, str):
            size = utils.get_size(found)
        else:
            size = sum([utils.get_size(f) for f in found])
        if size > self.configs.max_size_at_once:
            logger.error('''Size of this staff too large. If you want to move such a big things
                            you need to increase max_size_at_once in configs''')
            sys.exit(1)

        return size

    # wrappers over Trash API
    def move(self, path):
        utils.can_be_removed(path)
        size = self.size_checker(path)
        if not self.trash.have_space_for(size):
            removed = self.trash.free_space(size)
            printer.print_simple_entries(removed, 'removed in order to free space:', 'removed')
        moved = self.trash.move(path)
        printer.print_simple_entry(moved, 'moved')

    def restore(self, partial_id, on_collision='increment_number'):
        if on_collision not in config.RESTORE_COLLISION_CHOICES:
            logger.error('invalid on collision choice')
            sys.exit(1)
        result = self.trash.restore(partial_id, on_collision)
        printer.print_restored_entry(result)

    def remove(self, partial_id):
        result = self.trash.remove(partial_id)
        printer.print_simple_entry(result, 'removed')

    def get_all_with_shortest_ids(self):
        result = self.trash.get_all_with_shortest_ids()
        if result:
            printer.print_entries(result)
        else:
            logger.info('Trash is empty')

    def clear(self):
        result = self.trash.get_all_with_shortest_ids()
        for r in result:
            self.remove(r.id)
        logger.info('trash is empty now')

    def complete_remove(self, path):
        utils.can_be_removed(path)
        self.size_checker(path)
        result = self.trash.complete_remove(path)
        printer.print_simple_entry(result, 'completely removed')

    # complex operations with compositions of Trash API methods

    def move_by_regex(self, regex, path='.'):
        found = utils.find_by_regex(regex, path)
        self.size_checker(found)
        if not found:
            return logger.info('nothing found by this regex {0}'.format(regex))
        # printer.print_found_by_regex(regex, found)
        for f in found:
            self.move(f)

    def complete_remove_by_regex(self, regex, path='.'):
        found = utils.find_by_regex(regex, path)
        self.size_checker(found)
        if not found:
            return logger.info('nothing found by this regex {0}'.format(regex))
        printer.print_found_by_regex(regex, found)
        for f in found:
            self.complete_remove(f)

    def trash_size_info(self):
        total_size = self.trash.db.total_size()
        max_size = self.trash.size
        number_of_entries = len(self.trash.db.get_all())
        print 'total size: {0}'.format(utils.in_readable_size(total_size))
        print 'free space in trash: {0}'.format(utils.in_readable_size(max_size-total_size))
        print 'number of entries: {0}'.format(number_of_entries)

    def trash_only(self, number):
        all_entries = self.trash.get_all_with_shortest_ids()
        if all_entries > number:
            sorted_by_time = sorted(all_entries, key=lambda k: k.time)
            all_entries = sorted_by_time[:number]
        printer.print_entries(all_entries)