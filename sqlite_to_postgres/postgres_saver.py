import re
from contextlib import contextmanager
from dataclasses import astuple
from typing import Generator

import psycopg2
from psycopg2.extras import DictCursor, execute_values

from config import CONFIG


@contextmanager
def postgres_conn_context(dsl):
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield conn
    conn.close()


@contextmanager
def postgres_cursor_context(conn: psycopg2.connect):
    cursor = conn.cursor()
    yield cursor
    cursor.close()


BATCH_SIZE = CONFIG["BATCH_SIZE"]


class PostgresSaver:
    def __init__(self, conn):
        self.conn = conn

    def save_data(
        self,
        table: str,
        data: Generator[list, None, None],
        batch_size: int = BATCH_SIZE,
        schema: str = "content",
    ):
        fields = None
        with postgres_cursor_context(self.conn) as cur:
            for batch in data:
                rows = []
                if not fields:
                    fields = ", ".join(batch[0].__dataclass_fields__.keys())
                    fields = re.sub("created_at", "created", fields)
                    fields = re.sub("updated_at", "modified", fields)
                    query = """
                    INSERT INTO {schema}.{table} ({fields})
                    VALUES %s
                    ON CONFLICT (id) DO NOTHING
                    """.format(
                        schema=schema, table=table, fields=fields
                    )
                for row in batch:
                    rows.append(astuple(row))
                    execute_values(cur, query, rows, page_size=batch_size)
                    self.conn.commit()
