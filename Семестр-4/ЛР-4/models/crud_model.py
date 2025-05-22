import os
import datetime
import sqlite3
from patterns.patterns import Singleton
# from app import DB_PATH

DB_NAME:    str = 'logtable'
DB_FILE:    str = 'logtable.db'

FILE_PATH:  str = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH:  str = os.path.dirname(FILE_PATH)
DB_PATH:    str = os.path.join(ROOT_PATH, 'db')
DB_PATH:    str = os.path.join(DB_PATH, DB_FILE)


class CRUDModel(metaclass=Singleton):
    def __init__(self, db_log_path: str = DB_PATH, db_name: str = DB_NAME):
        self._table_name: str = db_name
        self.__con: sqlite3.Connection = sqlite3.connect(db_log_path, check_same_thread=False) # WARNING: this is unsafe TODO: db_connector?
        self.__create_table()

    # make lock logic for async?
    # no - singleton

    def __create_table(self) -> None:
        self.__con.execute(f"CREATE TABLE IF NOT EXISTS {self._table_name} (currency_code TEXT PRIMARY KEY , rate FLOAT, datetime TEXT)")
        self.__con.commit()
    
    # Deprecated. Reason: use by deprecated _create
    def _read_char_codes(self) -> list[str]:
        return [char_code[0] for char_code in self.__con.execute(f"SELECT currency_code FROM {self._table_name}")]

    # Deprecated. Reason: _upsert
    def _create(self, currencies: list[dict[str, float, str]]) -> None:
        # currency = [
        #               {'char_code': 'USD', 'rate': 90, 'datetime': '02-04-2025 11:10'},
        #               {'char_code': 'EUR', 'rate': 91, 'datetime': '02-04-2025 11:11'},
        #               {'char_code': 'GBP', 'rate': 100, 'datetime': '02-04-2025 11:37'}
        #            ]
        currencies_in_db: list[str] = self._read_char_codes()
        currencies = [currency for currency in currencies if currency['char_code'] not in currencies_in_db]
        
        if not currencies:
            return
            
        __sqlquery = f"INSERT INTO {self._table_name} (currency_code, rate, datetime) VALUES(?, ?, ?)"
        __data = [(currency['char_code'], currency['rate'], currency['datetime']) for currency in currencies]

        self.__con.executemany(__sqlquery, __data)
        self.__con.commit()
    
    # Deprecated. Reason: _upsert
    def _update(self, currencies: list[dict[str, float, str]]) -> None:
        __sqlquery = f"UPDATE {self._table_name} SET rate = ?, datetime = ? WHERE currency_code = ?"
        __data = [(currency['rate'], currency['datetime'], currency['char_code']) for currency in currencies]
        self.__con.executemany(__sqlquery, __data)
        self.__con.commit()
    
    def _read(self) -> list[tuple[str, float, str]]:
        rates: list[tuple[str, float, str]] = list(
            self.__con.execute(f"SELECT * FROM {self._table_name}")
        )
        return rates
    
    def _delete(self, char_code: str) -> None:
        with self.__con:
            self.__con.execute(f"DELETE FROM {self._table_name} WHERE currency_code = ?", (char_code,))

    def _upsert(self, currencies: list[dict[str, float, str]]) -> None:
        sqlquery = f"""
            INSERT INTO {self._table_name} (currency_code, rate, datetime)
            VALUES (?, ?, ?)
            ON CONFLICT(currency_code)
            DO UPDATE SET
                rate = excluded.rate,
                datetime = excluded.datetime
        """
        data = [(c["char_code"], c["rate"], c["datetime"]) for c in currencies]
        
        with self.__con:
            self.__con.executemany(sqlquery, data)

    @property
    def table_name(self) -> str:
        return self._table_name

    @table_name.setter
    def table_name(self, new_table_name: str) -> None:
        self._table_name = new_table_name
        self.__create_table()
