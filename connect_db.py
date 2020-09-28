import sqlite3


def db_connect(db):
    con = sqlite3.connect(db)
    return con
