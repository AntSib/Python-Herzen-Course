import os
import functools
import contextlib
import datetime
import sqlite3
from patterns import Singleton


FILE_PATH:  str = os.path.dirname(os.path.realpath(__file__))

db_log:     str = 'logtable.db'
db_log_path:   str = os.path.join(FILE_PATH, db_log)


@contextlib.contextmanager
def db_connector(con: sqlite3.Connection) -> sqlite3.Connection:
    """
    Context manager for database connection.

    Args:
        con: sqlite3.Connection - Connection to SQLite database.

    Yields:
        sqlite3.Connection - Connection to SQLite database.

    Notes:
        Creates 'logtable' table if it does not exist.
        Commits changes after leaving the context.
    """
    con.execute('''CREATE TABLE IF NOT EXISTS logtable (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        datetime TEXT,
                                        func_name TEXT,
                                        params TEXT,
                                        result TEXT
                                    )''')
    try:
        yield con
    finally:
        con.commit()
        con.close()


class Model(metaclass=Singleton):
    def __init__(self, db_log_path: str = db_log_path) -> None:
        self._db_log_path = db_log_path
        self._db_connection = sqlite3.connect(db_log_path)

    # make lock logic for async


    def write_to_db(self, table_name: str = 'logtable', value: str = None) -> None:
        with db_connector(self._db_connection) as con:
            pass
            # con.execute(f"INSERT INTO logtable (datetime, func_name, params, result) VALUES ('{datetime.datetime.now()}', '{func_name}', '{params}', '{result}')")

    def read_from_db(self, value: str = '*') -> None:
        with db_connector(self._db_connection) as con:
            cur = con.execute(f"SELECT {value} FROM logtable") # this is REALLY insafe
            for row in cur:
                print(row)
    
    def delete_from_db(self, data_type: str, value: str) -> None:
        with db_connector(self._db_connection) as con:
            con.execute(f"DELETE FROM logtable WHERE {data_type} = {value}")
    
    def update_in_db(self, data_type: str, value: str, new_value: str) -> None:
        with db_connector(self._db_connection) as con:
            con.execute(f"UPDATE logtable SET {data_type} = {new_value} WHERE {data_type} = {value}")

    # def create is not needed, because we have create logic in db_connector
    # def update
    # def read
    # def delete

    @property
    def db_log_path(self) -> str:
        return self._db_log_path

    @db_log_path.setter
    def db_log_path(self, db_log_path: str) -> None:
        self._db_log_path = db_log_path

    @property
    def db_connection(self) -> sqlite3.Connection:
        return self._db_log

    @db_connection.setter
    def db_connect(self, db_connect: sqlite3.Connection) -> None:
        self._db_log = db_connect


class ValuteRate(metaclass=Singleton):
    def __init__(self) -> None:
        self._valute_name: str = ''
        self._valute_rate: float = 0
    


if __name__ == '__main__':


    # model = Model()
    pass
