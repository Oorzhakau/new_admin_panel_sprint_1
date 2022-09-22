import sqlite3

from psycopg2.extensions import connection as _connection

from postgres_saver import PostgresSaver, postgres_conn_context
from sqlite_extractor import SQLiteExtractor, sqlite_conn_context


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres."""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    tables = sorted(sqlite_extractor.get_tables(), key=lambda x: len(x))
    for table in tables:
        data = sqlite_extractor.extract_data(table=table)
        postgres_saver.save_data(schema="content", table=table, data=data)


if __name__ == "__main__":
    from config import DSL

    with sqlite_conn_context(
        "db.sqlite"
    ) as sqlite_conn, postgres_conn_context(DSL) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
