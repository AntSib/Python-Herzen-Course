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

def json_logger(log_file: str) -> json:
    """
    Reads JSON data from a specified log file, if it exists.
    If the file does not exist or contains invalid JSON, an empty list is returned.

    Args:
        log_file: str - The path to the JSON log file.

    Returns:
        list - A list of parsed JSON.
    """

    if os.path.exists(log_file):    # safe read
        with open(log_file, 'r', encoding='utf-8') as h:
            try:
                json_data = json.load(h)
            except json.JSONDecodeError:
                json_data = []
    else:
        json_data = []

    return json_data


def trace(func: callable = None, *, handle: io.TextIOWrapper | str | sqlite3.Connection = sys.stdout) -> callable:
    """
    A decorator that logs the input, output, and execution details of a function.

    This decorator can log the information to various targets specified by the `handle` argument:
    - `sys.stdout`: Writes logs to console.
    - `<filepath>.json`: Appends logs in JSON format to the specified file.
    - `sqlite3.Connection`: Logs are stored in specified SQLite database table.
    
    Args:
        func: The function to be decorated.
        handle: The destination for logging. Can be an `sys.stdout`, a filepath string ending in '.json', 
                or an `sqlite3.Connection` object. Defaults to `sys.stdout`.

    Returns:
        A wrapper function that logs input, output, execution time, and other details of the decorated function.
    
    Raises:
        Exception: If the handle is unsupported or an unknown type.
    """

    if func is None:
        return lambda func: trace(func, handle=handle)
    
    @functools.wraps(func)
    def inner(*args, **kwargs) -> None:
        result = func(*args, **kwargs)
        datetime_now = datetime.datetime.now()
    
        if isinstance(handle, io.TextIOWrapper):    # io.TextIOWrapper case
            handle.write(f"{str(func.__name__)}({str((*args, *kwargs))}) -> {str(result)}\n")
        elif isinstance(handle, str):               # str case
            if handle.partition('.')[-1] == 'json':
                json_data = json_logger(handle)
                json_data.append({'datetime': str(datetime_now), 'func_name': str(func.__name__), 'params': str((*args, kwargs)), 'result': str(result)})
                with open(handle, 'w') as h:
                    json.dump(json_data, h, indent=4)
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
            raise Exception(ValueError("Unsupported type of handle: %s" % type(handle)))

        return func(*args, **kwargs)

    return inner


def showlogs(log_file: str) -> None:
    """
    Reads logs from the specified file and prints them to the console.

    Args:
        log_file: str - The file path of the log file. The file should have a '.json' or '.db' extension.

    Raises:
        Exception: If the file does not exist or cannot be read.
    """
    if log_file.partition('.')[-1] == 'json':
        try:
            with open(log_file, 'r') as f:
                json_data = f.readlines()
                for line in json_data:
                    print(line.strip())
        except Exception as err:
            print(f"Error accured while reading json: {err}")
        finally:
            return # exits function to not waste time on further processing
            
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
            return # exits function to not waste time on further processing
    else:
        print("Wrong extension of handle. Expected: 'json' or 'db', got: %s" % log_file.partition('.')[-1])


### Functions for test purposes
@trace(handle=sys.stdout)
def f0(x):
    return x + 1

@trace(handle=json_log_path)
def f1(x):
    return x + 2

@trace(handle=sqlite3.connect(db_log_path))
def f2(x):
    return x + 3
###

if __name__ == '__main__':
    f0(5)
    f1(10)
    f2(15)
    
    showlogs(db_log_path)
    showlogs(json_log_path)
