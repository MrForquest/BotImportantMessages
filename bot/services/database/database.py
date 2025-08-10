import sqlite3

import config

__factory = None


def global_init(db_path):
    global __factory
    connection = sqlite3.connect(str(db_path))

    def cursor_maker():
        return connection.cursor()

    __factory = cursor_maker


def get_cursor() -> sqlite3.Cursor:
    global __factory
    if not __factory:
        global_init(config.DATABASE_PATH)

    return __factory()


"""
None 2733191945280
None 2733198411232
None 2733198411232
None 2733191945280

"""
