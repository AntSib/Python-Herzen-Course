import sys, os, io
import functools
import contextlib
import datetime
import json
import sqlite3


FILE_PATH:  str = os.path.dirname(os.path.realpath(__file__))

json_log:   str = 'logger.json'
db_log:     str = 'logtable.db'

json_log_path: str = os.path.join(FILE_PATH, json_log)
db_log_path:   str = os.path.join(FILE_PATH, db_log)


@contextlib.contextmanager
def db_connector(con: sqlite3.Connection) -> sqlite3.Connection:
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


def trace(func: callable = None, *, handle: io.TextIOWrapper | str | sqlite3.Connection = sys.stdout) -> callable:
    if func is None:
        return lambda func: trace(func, handle=handle)
    
    @functools.wraps(func)
    def inner(*args, **kwargs) -> None:
        result = func(*args, **kwargs)
        datetime_now = datetime.datetime.now()
    
        if isinstance(handle, io.TextIOWrapper):     # io.TextIOWrapper case
            handle.write(f"{str(func.__name__)}({str((*args, *kwargs))}) -> {str(result)}\n")
        elif isinstance(handle, str):                # str case
            if handle.partition('.')[-1] == 'json':
                with open(handle, 'a') as h:
                    h.write(json.dumps({'datetime': str(datetime_now), 'func_name': str(func.__name__), 'params': str((*args, kwargs)), 'result': str(result)}) + '\n')
            else:
                raise Exception(ValueError(f"Wrong extension of handle. Expected: 'json', got: {handle.partition('.')[-1]}"))
        elif isinstance(handle, sqlite3.Connection): # sqlite3.Connection case
            with db_connector(handle) as con:
                con.execute("INSERT INTO logtable (datetime, func_name, params, result) VALUES (?, ?, ?, ?)",
                                    (
                                        str(datetime_now),
                                        str(func.__name__), 
                                        str((*args, *kwargs)), 
                                        str(result)
                                    )
                                )
        else:
            raise Exception(ValueError("Unknown type of handle: %s" % type(handle)))

        return func(*args, **kwargs)

    return inner



@trace(handle=sys.stdout)
def f0(x):
    return x + 1

@trace(handle=json_log_path)
def f1(x):
    return x + 2

@trace(handle=sqlite3.connect(db_log_path))
def f2(x):
    return x + 3

def showlogs(log_file):
    if log_file.partition('.')[-1] == 'json':
        try:
            with open(log_file, 'r') as f:
                json_data = f.readlines()
                for line in json_data:
                    print(line.strip())
        except Exception as err:
            print(f"Error accured while reading json: {err}")
        finally:
            return
            
    elif log_file.partition('.')[-1] == 'db':
        try:
            connection = sqlite3.connect(log_file)
        except sqlite3.OperationalError:
            print("sqlite3.OperationalError: Failed to connect to database")
        else:
            with db_connector(connection) as con:
                cur = con.execute("SELECT * FROM logtable")
                for row in cur:
                    print(row)
        finally:
            return
    else:
        print("Wrong extension of handle. Expected: 'json' or 'db', got: %s" % log_file.partition('.')[-1])
            

if __name__ == '__main__':
    # f0(0)
    # f1(20)
    # f2(15)
    
    # showlogs(db_log_path)
    # showlogs(json_log_path)
    pass
