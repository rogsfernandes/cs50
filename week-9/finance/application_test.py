import sqlite3

import pytest


@pytest.fixture()
def load_sql_file():
    with open('./sql/description.sql') as sql_file:
        sql_commands = sql_file.read()

    yield sql_commands


@pytest.fixture
def setup_db(load_sql_file):
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    create_sql = load_sql_file
    cursor.executescript(create_sql)
    cursor.execute('INSERT INTO users (username, hash) VALUES (\'roger\', \'12345\');')
    cursor.execute('INSERT INTO stocks (name, symbol) VALUES (\'Netflix Inc\', \'NFLX\');')
    cursor.execute('INSERT INTO transactions (user_id, stock_id, quantity, price, total, type) VALUES (1, 1, 1, 150, '
                   '150, \'buy\')')

    yield cursor


def test_app(setup_db):
    cursor = setup_db
    assert len(list(cursor.execute('SELECT * FROM users'))) == 1
