import os
import sqlite3

from entry import Entry


def to_entry(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if isinstance(result, list):
            return [Entry(*t) for t in result]
        if isinstance(result, tuple):
            return Entry(*result)
        return result
    return wrapper


class TrashSQL(object):
    def __init__(self, path):
        self.db_name = 'trash.db'
        db = os.path.join(path, self.db_name)
        self.connection = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
        self.__create_db_if_not_exist()

    def __create_db_if_not_exist(self):
        sql = '''create table if not exists trash
            (location  text                   not null,
            time      timestamp               not null,
            size      integer                 not null,
            id        char(32)  primary key   not null)'''
        self.cursor.execute(sql)
        self.connection.commit()

    def clear(self):
        sql = 'delete from trash'
        self.cursor.execute(sql)
        self.connection.commit()

    def create(self, entry):
        sql = 'insert into trash values (?, ?, ?, ?)'
        self.cursor.execute(sql, entry.to_tuple())
        self.connection.commit()

    # takes a list of dicts
    def create_many(self, entries):
        entries = [e.to_tuple() for e in entries]
        sql = 'insert into trash values (?, ?, ?, ?)'
        self.cursor.executemany(sql, entries)
        self.connection.commit()

    def remove(self, id):
        sql = 'delete from trash where id=?'
        self.cursor.execute(sql, (id,))
        self.connection.commit()

    @to_entry
    def get_by_partial_id(self, partial_id):
        sql = 'select * from trash where id like ?'
        self.cursor.execute(sql, (partial_id + '%',))

        return self.cursor.fetchall()

    def remove_by_partial_id(self, partial_id):
        sql = 'delete from trash where id like ?'
        self.cursor.execute(sql, (partial_id + '%',))
        self.connection.commit()

    @to_entry
    def get(self, id):
        sql = 'select * from trash where id=?'
        self.cursor.execute(sql, (id,))

        return self.cursor.fetchone()

    @to_entry
    def get_all(self):
        sql = 'select * from trash'
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def get_oldest_with_sum_of_sizes(self, size):
        all_entries = self.get_all()
        all_sorted = sorted(all_entries, key=lambda k: k.time)
        res = []
        for e in all_sorted:
            size -= e.size
            res.append(e)
            if size < 1:
                break

        return res

    def total_size(self):
        sql = 'select sum(size) from trash'
        self.cursor.execute(sql)
        res = self.cursor.fetchone()[0]
        if res is None:
            return 0
        return res
