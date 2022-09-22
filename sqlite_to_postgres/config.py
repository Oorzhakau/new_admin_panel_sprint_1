import os

from dotenv import load_dotenv

load_dotenv()

CONFIG = {"BATCH_SIZE": 100}

DSL = {
    "dbname": os.getenv("PG_DB_NAME", "movies_database"),
    "user": os.getenv("PG_DB_USER", "app"),
    "password": os.getenv("PG_DB_PASS", "123qwe"),
    "host": os.getenv("PG_DB_HOST", "127.0.0.1"),
    "port": os.getenv("PG_DB_PORT", "5432"),
}
