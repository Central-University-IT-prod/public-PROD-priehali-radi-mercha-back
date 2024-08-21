import sqlite3

connection = sqlite3.connect("database/database.db")


def is_open(conn):
    try:
        conn.cursor().close()
        return True
    except:
        return False


def get_connection():
    global connection
    if not is_open(connection):
        connection = sqlite3.connect("database/database.db")
    return connection
