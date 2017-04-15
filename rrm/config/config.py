import os

import fields
from collections import OrderedDict
from ..core import utils

CONFIG_LOCATION = os.path.join(os.path.expanduser('~'), '.rrm.json')

TRASH_NAME = '.rrm_trash'
CRON_COMMENT = 'scheduled rrm clear'
CRON_COMMAND = '/usr/local/bin/rrm -clear'

LOG_LOCATION = os.path.join(os.path.expanduser('~'), '.rrm.log')

RESTORE_COLLISION_CHOICES = ('replace_old', 'do_not_restore', 'increment_number')
LOG_LEVELS = ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET')
CLEAR_EACH = ('minute', 'hour', 'day', 'month', 'never')
MAX_TRASH_SIZE = utils.in_bytes(10, 'gb')
HELP_LINE_IN_CONFIG = 'json: http://www.json.org'


class BaseConfig(object):
    trash_location = fields.PathField(os.path.expanduser('~'))
    trash_size = fields.SizeField(utils.in_bytes(1, 'gb'), MAX_TRASH_SIZE)
    remove_oldest_when_out_of_space = fields.BooleanField(True)
    restore_collision = fields.ChoiceField('increment_number', RESTORE_COLLISION_CHOICES)
    level_for_log_in_file = fields.ChoiceField('DEBUG', LOG_LEVELS)
    level_for_log_in_terminal = fields.ChoiceField('INFO', LOG_LEVELS)
    clear_each = fields.ChoiceField('minute', CLEAR_EACH)
    max_size_at_once = fields.SizeField(utils.in_bytes(1, 'gb'), MAX_TRASH_SIZE)


class Config(BaseConfig):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if k in self.as_dict and not BaseConfig.__dict__[k].value == v:
                setattr(self, k, v)

    def get_help_for_field(self, field):
        if field in self.__dict__:
            return self.__dict__[field].help
        elif field in BaseConfig.__dict__:
            return BaseConfig.__dict__[field].help
        else:
            return 'no help'

    @property
    def as_dict(self):
        result = {}
        for name, attr in BaseConfig.__dict__.iteritems():
            if isinstance(attr, fields.Field):
                result[name] = attr.value
        for name, attr in self.__dict__.iteritems():
            if name in result:
                result[name] = attr.value

        return result

    def __eq__(self, other):
        return self.as_dict == other.as_dict


class JSONConfig(Config):
    def __init__(self, location=CONFIG_LOCATION, write=True):
        self.location = location
        params = {}
        if os.path.exists(location):
            try:
                params = utils.read_from_json(location)
                params = utils.phytonize_dict(params)
            except:
                pass
        Config.__init__(self, **params)
        if write:
            self.write_pretty()

    def write_pretty(self):
        configs = dict(self.as_dict)
        properties = {k: self.get_help_for_field(k) for k in configs}
        configs.update({'!help!': HELP_LINE_IN_CONFIG})
        configs.update({'!properties!': properties})
        utils.write_json_in_file(self.location, utils.humanize_dict(configs))
