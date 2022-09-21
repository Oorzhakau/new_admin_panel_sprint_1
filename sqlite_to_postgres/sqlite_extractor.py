import sqlite3
from contextlib import contextmanager
from typing import Generator

from config import CONFIG
from dataclass import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@contextmanager
def sqlite_conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@contextmanager
def sqlite_cursor_context(conn: sqlite3.Connection):
    cursor = conn.cursor()
    yield cursor
    cursor.close()


BATCH_SIZE = CONFIG["BATCH_SIZE"]


class SQLiteExtractor:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self._dataclass = {
            "genre": {
                "dataclass": Genre,
            },
            "film_work": {
                "dataclass": Filmwork,
            },
            "person": {
                "dataclass": Person,
            },
            "genre_film_work": {
                "dataclass": GenreFilmwork,
            },
            "person_film_work": {
                "dataclass": PersonFilmwork,
            },
        }

    def get_tables(self) -> list:
        """Метод для получения всех названий таблиц в базе SQLite."""

        with sqlite_cursor_context(self.conn) as cur:
            query = "SELECT name FROM sqlite_master WHERE type='table'"
            cur.execute(query)

            tables = [row["name"] for row in cur.fetchall()]
        return tables

    def extract_data(
        self, table: str, batch_size: int = BATCH_SIZE
    ) -> Generator[list, None, None]:
        """Метод получения батча данных из указанной таблицы."""
        with sqlite_cursor_context(self.conn) as cur:
            query = f"SELECT * FROM {table}"
            cur.execute(query)
            while True:
                batch = cur.fetchmany(batch_size)
                if not batch:
                    break
                data = [
                    self._dataclass[table]["dataclass"](**row) for row in batch
                ]
                yield data
