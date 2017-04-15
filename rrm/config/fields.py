import os


class Field(object):
    def __init__(self, default):
        if not self.validate(default):
            raise TypeError('not valid type for this field')
        self.value = default

    def validate(self, value):
        return True

    @property
    def help(self):
        return 'help'

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if self.validate(value):
            self.value = value


class PathField(Field):
    def validate(self, value):
        return os.path.exists(value)

    @property
    def help(self):
        return {
            'info': 'path to directory or file',
            'type': 'string'
        }


class SizeField(Field):
    def __init__(self, default, max_size):
        self.max_size = max_size
        Field.__init__(self, default)

    def validate(self, value):
        return isinstance(value, int) and -1 < value < self.max_size

    @property
    def help(self):
        return {
            'info': 'size in bytes (from 0 to {0})'.format(self.max_size),
            'type': 'number'
        }

class BooleanField(Field):
    def validate(self, value):
        return isinstance(value, bool)

    @property
    def help(self):
        return {
            'type': 'boolean'
        }


class ChoiceField(Field):
    def __init__(self, default, choices):
        self.choices = choices
        Field.__init__(self, default)

    def validate(self, value):
        return value in self.choices

    @property
    def help(self):
        return {
            'choices': self.choices,
            'type': 'string'
        }


