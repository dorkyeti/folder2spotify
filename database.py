import sqlite3
from argsparse import args


def _dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


conn = sqlite3.connect(
    args.database,
    detect_types=sqlite3.PARSE_DECLTYPES
)
conn.row_factory = _dict_factory
sqlite3.register_adapter(bool, int)
sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

conn.cursor().executescript("""CREATE TABLE IF NOT EXISTS music(
    id INTEGER PRIMARY KEY,
    artist TEXT,
    title TEXT,
    album TEXT,
    spotify_id TEXT,
    is_uploaded BOOLEAN,
    path TEXT
);
""")


def _build_insert_query(table, columns):
    fields = ''
    values = ''

    for field in columns:
        fields += '{}, '.format(field)
        values += ':{}, '.format(field)

    return 'INSERT INTO {} ({}) VALUES ({})'.format(table, fields[:-2], values[:-2])


def _build_update_query(table, columns):
    fields = ''

    for field in columns:
        if (field == 'id'):
            continue

        fields += '{0}=:{0}, '.format(field)

    return 'UPDATE {} SET {} WHERE id=:id'.format(table, fields[:-2])


def insert(table, data):
    sql = _build_insert_query(table, data.keys())
    with conn:
        return conn.execute(sql, data)


def insert_many(table, data):
    sql = _build_insert_query(table, data[0].keys())
    with conn:
        cursor = conn.executemany(sql, data)
        return cursor.rowcount


def select(query, as_cursor=False):
    response = conn.execute(query)

    if as_cursor:
        return response

    return response.fetchall()


def select_one(query):
    response = conn.execute(query)

    return response.fetchone()


def update_one(table, item):
    sql = _build_update_query(table, item.keys())

    with conn:
        cursor = conn.execute(sql, item)
        return cursor.rowcount
