"""manager of trash directory"""

import os
import shutil

import utils
from entry import Entry
from error import TrashError
from trash_sql import TrashSQL


class Trash(object):
    def __init__(self, location, size):
        self.location = location
        utils.create_directory_if_not_exists(self.location)
        self.db = TrashSQL(self.location)
        self.size = size
        self.dry = False

    def have_space_for(self, size):
        free_space = self.size - self.db.total_size()

        return free_space > size

    def free_space(self, size):
        for_removal = self.db.get_oldest_with_sum_of_sizes(size)

        return [self.remove(r.id) for r in for_removal]

    def move(self, path):
        utils.can_be_removed(path)
        entry = Entry(path)
        if not self.dry:
            dist = os.path.join(self.location, entry.id)
            utils.move(entry.location, dist)
            self.db.create(entry)

        return entry

    def get_from_db(self, partial_id):
        entries = self.db.get_by_partial_id(partial_id)
        if len(entries) != 1:
            raise TrashError('wrong id')

        return entries[0]

    def restore(self, partial_id, on_collision='increment_number'):
        entry = self.get_from_db(partial_id)
        if not self.dry:
            self.db.remove_by_partial_id(partial_id)
            entry.location = utils.move(os.path.join(self.location, entry.id), entry.location, on_collision)

        return entry

    def remove(self, partial_id):
        entry = self.get_from_db(partial_id)
        if not self.dry:
            self.db.remove_by_partial_id(partial_id)
            utils.remove_file_or_dir(os.path.join(self.location, entry.id))

        return entry

    def get_all_with_shortest_ids(self):
        all_entries = self.db.get_all()
        if all_entries:
            ids = [d.id for d in all_entries]
            min_len = utils.get_minimal_unique_len(ids)
            for entry in all_entries:
                entry.id = entry.id[:min_len]

        return all_entries

    def complete_remove(self, path):
        entry = Entry(path)
        if not self.dry:
            shutil.rmtree(path)

        return entry

