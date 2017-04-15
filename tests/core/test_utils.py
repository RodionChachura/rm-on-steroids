import json
import os
import shutil
import tempfile
import unittest

from .. import mocks
from rrm.core import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_create_directory(self):
        new_dir = os.path.join(self.test_dir, 'new_test')
        utils.create_directory(new_dir)
        new_dir_created = os.path.basename(new_dir) in os.listdir(self.test_dir)
        self.assertTrue(new_dir_created)

    def test_write_json_in_file(self):
        new_file = os.path.join(self.test_dir, 'new_file.json')
        utils.write_json_in_file(new_file, mocks.for_json)
        new_json_created = os.path.basename(new_file) in os.listdir(self.test_dir)
        self.assertTrue(new_json_created)
        with open(new_file) as f:
            readed_data = json.load(f)
        self.assertEqual(mocks.for_json, readed_data)

    def test_read_from_json(self):
        new_file = os.path.join(self.test_dir, 'new_file.json')
        utils.write_json_in_file(new_file, mocks.for_json)
        readed_data = utils.read_from_json(new_file)
        self.assertEqual(mocks.for_json, readed_data)
        pass

    def test_minimal_unique_len(self):
        for k, v in mocks.partial_ids.iteritems():
            res = utils.get_minimal_unique_len(v)
            self.assertEqual(res, int(k))

    def test_get_size(self):
        mb = 1048575

        def make_temp_file(dir=self.test_dir, size_in_mb=1):
            file = tempfile.NamedTemporaryFile(dir=dir, delete=False)
            with open(file.name, 'w') as f:
                f.seek(size_in_mb * mb)
                f.write('0')
            return file

        temp_dir = tempfile.mkdtemp(dir=self.test_dir)
        make_temp_file()
        make_temp_file(size_in_mb=3)
        make_temp_file(dir=temp_dir, size_in_mb=2)
        expected = 6 * mb + 3
        result = utils.get_size(self.test_dir)
        self.assertEqual(expected, result)

    def test_find_by_regex(self):
        dir_1 = tempfile.mkdtemp(dir=self.test_dir)
        dir_2 = tempfile.mkdtemp(dir=self.test_dir)
        dir_3 = tempfile.mkdtemp(dir=dir_1)
        tempfile.NamedTemporaryFile(suffix='.py', dir=self.test_dir, delete=False)
        tempfile.NamedTemporaryFile(suffix='.py', dir=dir_1, delete=False)
        tempfile.NamedTemporaryFile(suffix='.py', dir=dir_2, delete=False)
        tempfile.NamedTemporaryFile(suffix='.py', dir=dir_3, delete=False)
        expected = 4
        result = len(utils.find_by_regex('*.py', self.test_dir))
        self.assertEqual(expected, result)

    def test_set_number_in_path(self):
        path = 'guitar/drums/play.json'
        expected = 'guitar/drums/play2.json'
        result = utils.set_number_in_path(path, 2)
        self.assertEqual(expected, result)
        path = 'play/drums/play.json.json.json'
        expected = 'play/drums/play2.json.json.json'
        result = utils.set_number_in_path(path, 2)
        self.assertEqual(expected, result)
        path = '.log'
        expected = '2.log'
        result = utils.set_number_in_path(path, 2)
        self.assertEqual(expected, result)

    def test_move_with_empty(self):
        src = tempfile.mkdtemp(dir=self.test_dir)
        dist = os.path.join(self.test_dir, 'dist')
        utils.move(src, dist)
        self.assertEqual(os.listdir(self.test_dir), ['dist'])
        self.assertEqual(os.listdir(dist), [])

    def test_move_with_files(self):
        src = tempfile.mkdtemp(dir=self.test_dir)
        dist = os.path.join(self.test_dir, 'dist')
        file_in_src = tempfile.NamedTemporaryFile(dir=src, delete=False)
        dir_in_src = tempfile.mkdtemp(dir=src)
        file_in_dir_in_src = tempfile.NamedTemporaryFile(dir=dir_in_src, delete=False)
        utils.move(src, dist)
        self.assertListEqual(os.listdir(self.test_dir), ['dist'])
        self.assertListEqual(sorted(os.listdir(dist)), sorted([os.path.basename(file_in_src.name), os.path.basename(dir_in_src)]))
        dir_in_src = os.path.join(dist, os.path.basename(dir_in_src))
        self.assertListEqual(sorted(os.listdir(dir_in_src)), sorted([os.path.basename(file_in_dir_in_src.name)]))

    def test_in_readable_size(self):
        expected = '4.50kb'
        result = utils.in_readable_size(4608)
        self.assertEqual(expected, result)
        expected = '117.42mb'
        result = utils.in_readable_size(123123123)
        self.assertEqual(expected, result)
        expected = '9.31gb'
        result = utils.in_readable_size(9999999999)
        self.assertEqual(expected, result)

    def test_replace_keys_in_dict(self):
        expected = mocks.nested_dict_with_replace
        result = utils.replace_keys_in_dict(mocks.nested_dict, '_', ' ')
        self.assertEqual(expected, result)