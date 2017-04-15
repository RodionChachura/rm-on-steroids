import shutil
import tempfile
import unittest

from .. import mocks
from rrm.config import config


class TestConfig(unittest.TestCase):
    """
    mocking CONFIG CONSTANTS
    without mock library
    """
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.location = tempfile.NamedTemporaryFile(dir=self.test_dir, suffix='.json', delete=False).name

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_if_invalid_config(self):
        with open(self.location, 'w') as f:
            f.write(mocks.invalid_config)

        expected = config.Config()
        result = config.JSONConfig(self.location)
        self.assertEqual(result, expected)

    def test_must_fail_config(self):
        with open(self.location, 'w') as f:
            f.write(mocks.must_fail_config)

        expected = config.Config()
        result = config.JSONConfig(self.location)
        self.assertEqual(result, expected)

    def test_valid_config(self):
        with open(self.location, 'w') as f:
            f.write(mocks.must_fail_config)

        expected = config.Config(trash_location = '~/', trash_size = 666666666, show_process = True)
        result = config.JSONConfig(self.location)
        self.assertEqual(result, expected)

    def test_without_config(self):
        expected = config.Config()
        result = config.JSONConfig(self.location)
        self.assertEqual(result, expected)
