import sqlite3
import os
import sys


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("../"), relative_path)


def get_connection():
    connection = sqlite3.connect(resource_path('resources/remaster.db'))
    connection.row_factory = dict_factory

    try:
        yield connection
    finally:
        connection.close()
