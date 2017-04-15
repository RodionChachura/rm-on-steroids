import unittest
import tempfile
import os
import shutil

from rrm.core.trash_sql import TrashSQL

import tests.mocks


class TestTrashDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestTrashDB, cls).setUpClass()
        cls.test_dir = tempfile.mkdtemp()
        cls.db = TrashSQL(cls.test_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)
        super(TestTrashDB, cls).tearDownClass()

    def tearDown(self):
        self.db.clear()

    def test_db_creation(self):
        db_created = self.db.db_name in os.listdir(self.test_dir)
        self.assertTrue(db_created)

    def test_create_many(self):
        self.db.create_many(tests.mocks.entries)
        res = self.db.get_all()
        self.assertEqual(res, tests.mocks.entries)

    def test_clear(self):
        self.db.create_many(tests.mocks.entries)
        self.db.clear()
        res = self.db.get_all()
        self.assertEqual(res, [])

    def test_get_by_partial_id(self):
        self.db.create_many(tests.mocks.entries)
        expected = tests.mocks.entries[0]
        result = self.db.get_by_partial_id(expected.id[:1])
        self.assertEqual(expected, result[0])

    def test_create(self):
        entry = tests.mocks.entries[0]
        self.db.create(entry)
        from_db = self.db.get(entry.id)
        self.assertEqual(entry, from_db)

    def test_remove(self):
        entry = tests.mocks.entries[1]
        self.db.create(entry)
        self.db.remove(entry.id)
        from_db = self.db.get(entry.id)
        self.assertEqual(from_db, None)

    def test_remove_by_partial_id(self):
        self.db.create_many(tests.mocks.entries)
        for_removing = tests.mocks.entries[0]
        self.db.remove_by_partial_id(for_removing.id[0])
        removed = for_removing not in self.db.get_all()
        self.assertTrue(removed)

    def test_get_all(self):
        for entry in tests.mocks.entries:
            self.db.create(entry)
        from_db = self.db.get_all()
        self.assertEqual(from_db, tests.mocks.entries)

    def test_get_oldest_with_sum_of_sizes(self):
        self.db.create_many(tests.mocks.more_entries)
        sorted_by_time = sorted(tests.mocks.more_entries, key=lambda k: k.time)
        test_size = 12335730
        from_db = self.db.get_oldest_with_sum_of_sizes(test_size)
        expected = sorted_by_time[:2]
        self.assertEqual(from_db, expected)

    def test_total_size(self):
        self.db.create_many(tests.mocks.entries)
        result = self.db.total_size()
        expected = sum([x.size for x in tests.mocks.entries])
        self.assertEqual(result, expected)