from datetime import datetime
from rrm.core.entry import Entry
from rrm.config.config import Config


config = Config()

entries = [
    Entry(
        id='717b6d88c0140062e6ddbaf83d8b1bca',
        path='test/file1.json',
        time=datetime(2017, 4, 7, 18, 12, 30),
        size=12312
    ),
    Entry(
        id='db11ebd17f6a60f212b8c81d8114aa45',
        path='test/directory1',
        time=datetime(2017, 4, 2, 12, 12, 30),
        size=12312312
    ),
    Entry(
        id='led4e58531e9aaf7b0dbf7f1bd425c3a',
        path='test/file2.py',
        time=datetime(2017, 1, 18, 7, 23, 34),
        size=23423
    ),
    Entry(
        id='52a7dd5602d9f4ff59beccc24a44b461',
        path='test/directory2',
        time=datetime(2017, 6, 18, 7, 20, 34),
        size=23423423,
    )
]

more_entries = entries + [
    Entry(
        id='717b6d88c0140062e6ddbaf83d8brrrr',
        path='test/file8.json',
        time=datetime(2017, 9, 18, 7, 23, 34),
        size=12312,
    ),
    Entry(
        id='db11ebd17f6a60f212b8c81d811qqqqq',
        path='test/directory8',
        time=datetime(2017, 10, 2, 12, 12, 30),
        size=12312312,

    ),
    Entry(
        id='fed4e58531e9aaf7b0dbf7f1bd4xxxxx',
        path='test/file9.py',
        time=datetime(2017, 11, 18, 7, 23, 34),
        size=23423,
    ),
    Entry(
        id='52a7dd5602d9f4ff59beccc24a4zzzzz',
        path='test/directory9',
        time=datetime(2017, 12, 18, 7, 20, 34),
        size=23423423,
    )
]

partial_ids = {
    '1': ['qwer', 'asdf', 'xvcv'],
    '2': ['1234', '1345', '1456'],
    '3': ['a111', 'a122', 'a133'],
    '4': ['a123', 'a124', 'a125']
}

for_json = {
    'Van Halen': ['Eddie', 'Alex', 'Mark', 'Michael'],
    'KISS': ['Peter', 'Paul', 'Gene', 'Ace']
}

valid_config = '''
{
    "trash_location": "~/",
    "trash_size": 666666666,
    "show_process": true,
}
'''

invalid_config = '''
{
    "trash_location": "guitar/drams",
    "trash_size": "ronni",
    "show_process": [true, false]
}
'''

must_fail_config = '''
{
    "trash_location": 123abc,
    I can't drive 55 ...
}
'''


nested_dict = {
    'some_way': [
        {'one_1': 'one'},
        {'two_2': 'two'}
    ],
    'other_way': (
        {'three_3': 'three'},
        {'four_4': 'four'}
    ),
    'wild_way': (
        [
            {'some_some': 'some_some'}
        ]
    )
}

nested_dict_with_replace = {
    'some way': [
        {'one 1': 'one'},
        {'two 2': 'two'}
    ],
    'other way': [
        {'three 3': 'three'},
        {'four 4': 'four'}
    ],
    'wild way':[
        {'some some': 'some_some'}
    ]
}

