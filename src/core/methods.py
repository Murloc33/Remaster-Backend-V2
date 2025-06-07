import os
import sqlite3
import sys
from sqlite3 import Connection
from typing import Any, Generator


def dict_factory(cursor, row):
    record = {}

    for idx, col in enumerate(cursor.description):
        record[col[0]] = row[idx]

    return record


def resource_path(relative_path: str):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("../"), relative_path)


def get_connection() -> Generator[Connection, Any, None]:
    connection = sqlite3.connect(resource_path('resources/remaster.db'))
    connection.row_factory = dict_factory

    try:
        yield connection
    finally:
        connection.close()
