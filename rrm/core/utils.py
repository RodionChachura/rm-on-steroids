"""utils to simplify life"""
import sys
import os
import json
import shutil
import hashlib
import fnmatch
from error import TrashError

DIMENSIONS = {
    'b': 1,
    'kb': 1024,
    'mb': 1024 * 1024,
    'gb': 1024 * 1024 * 1024
}

ORDERED_DIMENSIONS = ('b', 'kb', 'mb', 'gb')


def create_directory(path):
    os.makedirs(path)


def write_json_in_file(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)


def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        create_directory(path)


def write_json_in_file_if_not_exists(path, data):
    if not os.path.exists(path):
        write_json_in_file(path, data)


def read_from_json(path):
    with open(path) as f:
        data = json.load(f)
        return data


def get_minimal_unique_len(ids):
    max_id = len(ids[0])
    for length in xrange(1, max_id):
        s = {s[:length] for s in ids}
        if len(s) == len(ids):
            return length

    return max_id


def remove_file_or_dir(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        raise ValueError('not a file or directory')


def set_number_in_path(path, number):
    if os.path.isdir(path):
        return path + str(number)
    name = os.path.basename(path)
    sep = name.split('.')
    if sep:
        sep[0] += str(number)
        new_name = '.'.join(sep)
    else:
        new_name = name + str(number)
    dirs = '/'.join(path.split('/')[:-1])

    return os.path.join(dirs, new_name)


def move(src, dist, on_collision='increment_number'):
    dirs = '/'.join(dist.split('/')[:-1])
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    if os.path.exists(dist):
        if on_collision == 'increment_number':
            i = 2
            while os.path.exists(dist):
                dist = set_number_in_path(dist, i)
                i += 1
        elif on_collision == 'replace_old':
            remove_file_or_dir(dist)
        elif on_collision == 'do_not_restore':
            return None
    shutil.move(src, dist)

    return dist


def get_size(path):
    size = 0
    if os.path.isfile(path):
        return os.path.getsize(path)
    for directory, _, files in os.walk(path):
        for f in files:
            file_path = os.path.join(directory, f)
            size += os.path.getsize(file_path)

    return size


def get_hash_str(*args):
    hash_obj = hashlib.md5(''.join(map(str, args)))

    return hash_obj.hexdigest()


def in_bytes(units, dimension):
    return units * DIMENSIONS[dimension]


def from_bytes(bytes, dimension):
    return bytes / DIMENSIONS[dimension]


def in_readable_size(bytes):
    bytes = abs(bytes)
    for v in ORDERED_DIMENSIONS:
        if bytes < 1024.0:
            return '%3.2f%s' % (bytes, v)
        bytes /= 1024.0


def can_be_removed(path):
    if not os.path.exists(path):
        raise TrashError('path does not exists')
    if os.path.dirname(path) == path:
        raise TrashError('system directory detected')

    return True


def find_by_regex(regex, location='.'):
    matches = []
    for root, dirs, files in os.walk(location):
        for filename in fnmatch.filter(files, regex):
            matches.append(os.path.join(root, filename))

    return matches


def make_silent():
    f = open(os.devnull, 'w')
    sys.stdout = f


def replace_keys_in_dict(dictionary, old, new):
    def recursive(d):
        if isinstance(d, (list, tuple)):
            return map(recursive, d)
        elif isinstance(d, dict):
            return {k.replace(old, new): recursive(v) for k, v in d.iteritems()}
        else:
            return d

    return recursive(dictionary)


def phytonize_dict(dictionary):
    return replace_keys_in_dict(dictionary, ' ', '_')


def humanize_dict(dictionary):
    return replace_keys_in_dict(dictionary, '_', ' ')


