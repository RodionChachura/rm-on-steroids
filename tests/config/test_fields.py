import unittest

from rrm.config import fields


class TestValidators(unittest.TestCase):

    def test_is_trash_location_valid(self):
        self.assertRaises(TypeError, fields.PathField, 'guitar/drums')

    def test_is_trash_size_valid(self):
        self.assertRaises(TypeError, fields.SizeField, -55, 66666666)
        self.assertRaises(TypeError, fields.SizeField, 'ronni', 66666666)

    def test_is_boolean_valid(self):
        self.assertRaises(TypeError, fields.BooleanField, 'ronni')
