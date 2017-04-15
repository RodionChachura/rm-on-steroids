import os
from datetime import datetime

import utils


class Entry(object):
    def __init__(self, path, time=None, size=None, id=None):
        self.location = os.path.abspath(path)
        self.time = time or datetime.now()
        self.size = size or utils.get_size(path)
        self.id = id or utils.get_hash_str(path, self.time)

    def to_tuple(self):
        return self.location, self.time, self.size, self.id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
