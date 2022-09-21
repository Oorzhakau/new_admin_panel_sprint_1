import os
import sqlite3

from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection

from postgres_saver import PostgresSaver, postgres_conn_context
from sqlite_extractor import SQLiteExtractor, sqlite_conn_context

load_dotenv()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres."""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    tables = sqlite_extractor.get_tables()
    for table in tables:
        data = sqlite_extractor.extract_data(table=table)
        postgres_saver.save_data(schema="content", table=table, data=data)


if __name__ == "__main__":
    dsl = {
        "dbname": os.getenv("PG_DB_NAME", "movies_database"),
        "user": os.getenv("PG_DB_USER", "movies_database"),
        "password": os.getenv("PG_DB_PASS", "123qwe"),
        "host": os.getenv("PG_DB_HOST", "127.0.0.1"),
        "port": os.getenv("PG_DB_PORT", "5432"),
    }
    with sqlite_conn_context(
        "db.sqlite"
    ) as sqlite_conn, postgres_conn_context(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
