import copy
import os
import shutil
import tempfile
import unittest

from .. import mocks

from rrm.core.trash import Trash
from rrm.core.utils import remove_file_or_dir


class TestTrash(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.trash_dir = tempfile.mkdtemp()
        self.trash = Trash(self.trash_dir, os.path.join(self.trash_dir, 'mock_trash'))

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.trash_dir)

    def test_move_in_trash_empty_directory(self):
        start_size = len(os.listdir(self.trash.location))
        temp = tempfile.mkdtemp(dir=self.test_dir)
        self.trash.move(temp)
        removed = os.path.basename(temp) not in os.listdir(self.test_dir)
        self.assertTrue(removed)
        final_size = len(os.listdir(self.trash.location))
        self.assertEqual(start_size+1, final_size)

    def test_move_in_trash_not_empty_directory(self):
        start_size = len(os.listdir(self.trash.location))
        temp_dir = tempfile.mkdtemp(dir=self.test_dir)
        tempfile.TemporaryFile(dir=temp_dir)
        self.trash.move(temp_dir)
        removed = os.path.basename(temp_dir) not in os.listdir(self.test_dir)
        self.assertTrue(removed)
        final_size = len(os.listdir(self.trash.location))
        self.assertEqual(start_size+1, final_size)

    def test_restore_directory_from_trash(self):
        temp_dir = tempfile.mkdtemp(dir=self.test_dir)
        id = self.trash.move(temp_dir).id
        self.assertFalse(os.path.exists(temp_dir))
        self.trash.restore(id)
        self.assertTrue(os.path.exists(temp_dir))

    def test_restore_file_with_content_from_trash(self):
        text = 'some text'
        file = tempfile.NamedTemporaryFile(dir=self.test_dir, delete=False)
        with open(file.name, 'w') as f:
            f.write(text)
        id = self.trash.move(file.name).id
        self.assertFalse(os.path.exists(file.name))
        self.trash.restore(id)
        self.assertTrue(os.path.exists(file.name))
        with open(file.name, 'r') as f:
            after_restore = f.read()
        self.assertEqual(after_restore, text)

    def test_restore_deep_directory(self):
        dir1 = tempfile.mkdtemp(dir=self.test_dir)
        dir2 = tempfile.mkdtemp(dir=dir1)
        dir3 = tempfile.mkdtemp(dir=dir2)

        id = self.trash.move(dir3).id
        remove_file_or_dir(dir1)
        self.trash.restore(id)
        restored = os.path.exists(dir3)
        self.assertTrue(restored)

    def test_get_all_with_shortest_ids(self):
        self.trash.db.clear()
        self.trash.db.create_many(mocks.entries)
        self.trash.get_all_with_shortest_ids()
        expected = copy.deepcopy(mocks.entries)
        for e in expected:
            e.id = e.id[:1]
        result = self.trash.get_all_with_shortest_ids()
        self.assertEqual(result, expected)

    def test_remove(self):
        temp_dir = tempfile.mkdtemp(dir=self.test_dir)
        id = self.trash.move(temp_dir).id
        self.trash.remove(id)
        removed = id not in os.listdir(self.trash.location)
        self.assertTrue(removed)

    def test_have_space_for(self):
        self.trash.size = 160000000000
        self.trash.db.create_many(mocks.entries[:2])
        result = self.trash.have_space_for(1599876753764)
        self.assertFalse(result)
