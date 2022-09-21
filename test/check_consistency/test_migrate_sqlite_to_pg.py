import os
import sqlite3
from datetime import datetime
from pathlib import Path

import psycopg2
import pytest
from dotenv import load_dotenv
from psycopg2.extras import DictCursor
from sqlite_to_postgres.postgres_saver import postgres_cursor_context
from sqlite_to_postgres.sqlite_extractor import sqlite_cursor_context

load_dotenv()

SQLITE_PATH = os.getenv("SQLITE_DB_PATH", "db.sqlite")
SQLITE_FULLPATH = (
    Path(__file__).resolve().parent.parent.parent
    / "sqlite_to_postgres"
    / SQLITE_PATH
)

PG_DSL = {
    "dbname": os.getenv("PG_DB_NAME", "movies_database"),
    "user": os.getenv("PG_DB_USER", "movies_database"),
    "password": os.getenv("PG_DB_PASS", "123qwe"),
    "host": os.getenv("PG_DB_HOST", "127.0.0.1"),
    "port": os.getenv("PG_DB_PORT", "5432"),
}


class TestClass:
    def setup_method(self):
        self.sqlite_conn = sqlite3.connect(SQLITE_FULLPATH)
        self.sqlite_conn.row_factory = sqlite3.Row
        self.pg_conn = psycopg2.connect(**PG_DSL, cursor_factory=DictCursor)

    def teardown_method(self):
        self.sqlite_conn.close()
        self.pg_conn.close()

    @pytest.mark.parametrize(
        "table,",
        [
            "film_work",
            "genre",
            "genre_film_work",
            "person",
            "person_film_work",
        ],
    )
    def test_eq_table(self, table: str):
        query = "SELECT COUNT(*) AS count FROM {table}".format(table=table)
        with sqlite_cursor_context(self.sqlite_conn) as cur:
            cur.execute(query)
            count_base = cur.fetchone()["count"]
        with postgres_cursor_context(self.pg_conn) as cur:
            cur.execute(query)
            count_replica = cur.fetchone()["count"]
        assert (
            count_base == count_replica
        ), "Sizes base and replica table not equalin." ' "{table}"'.format(
            table=table
        )

    @pytest.mark.parametrize(
        "table,",
        [
            "film_work",
            "genre",
            "genre_film_work",
            "person",
            "person_film_work",
        ],
    )
    def test_eq_rows_filmwork(self, table):
        query = f"SELECT * FROM {table}"
        with sqlite_cursor_context(
            self.sqlite_conn
        ) as sl_cur, postgres_cursor_context(self.pg_conn) as pg_cur:
            sl_cur.execute(query)
            pg_cur.execute(query)
            sl_data = sl_cur.fetchall()
            pg_data = pg_cur.fetchall()
            for sl_row, pg_row in zip(sl_data, pg_data):
                sl_row = dict(sl_row)
                pg_row = dict(pg_row)
                if "created_at" in sl_row:
                    date = sl_row["created_at"] + "00"
                    sl_row["created"] = datetime.strptime(
                        date, "%Y-%m-%d %H:%M:%S.%f%z"
                    )
                    sl_row.pop("created_at")
                if "updated_at" in sl_row:
                    date = sl_row["updated_at"] + "00"
                    sl_row["modified"] = datetime.strptime(
                        date, "%Y-%m-%d %H:%M:%S.%f%z"
                    )
                    sl_row.pop("updated_at")
                assert sl_row == pg_row, "rows doesn't equale"
