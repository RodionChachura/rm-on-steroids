import os
import logging

from ..core.utils import in_readable_size

logger = logging.getLogger(__name__)


def print_entries(entries):
    ids = map(lambda x: str(x.id), entries)
    locations = map(lambda x: x.location, entries)
    times = map(lambda x: x.time.strftime('%Y-%m-%d %H:%M:%S'), entries)
    sizes = map(lambda x: x.size, entries)

    id_len = len(max(ids, key=len))
    location_len = len(max(locations, key=len))
    time_len = len(times[0])
    if location_len > 50:
        location_len = 50
    size_len = 9
    entry_str = '{0:'+str(id_len)+'} {1:'+str(location_len)+'} {2:'+str(time_len)+'} {3:'+str(size_len)+'}'
    print entry_str.format('ID', 'LOCATION', 'TIME', 'SIZE')
    for i in range(len(entries)):
        print entry_str.format(ids[i], reduce_location(locations[i], location_len), times[i], in_readable_size(sizes[i]))


def reduce_location(location, size):
    prefix = '... '
    if len(location) < size:
        return location
    return prefix + location[-size + len(prefix):]

def print_simple_entry(entry, prefix=''):
    basename = os.path.basename(entry.location)
    logger.info('{0} {1} with size: {2}'.format(prefix, basename, in_readable_size(entry.size)))


def print_simple_entries(entries, common_prefix=None, prefix=''):
    if common_prefix:
        print common_prefix
    for e in entries:
        print_simple_entry(e, prefix)


def print_restored_entry(entry):
    logger.info('restored in location {0}'.format(entry.location))


def print_found_by_regex(regex, found):
    print 'by regex {0}'.format(regex)
    for f in found:
        print f
