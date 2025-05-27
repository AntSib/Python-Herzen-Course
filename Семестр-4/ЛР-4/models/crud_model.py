import os
import datetime
import sqlite3
from patterns.patterns import Singleton

DB_NAME:    str = 'logtable'
DB_FILE:    str = 'logtable.db'

FILE_PATH:  str = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH:  str = os.path.dirname(FILE_PATH)
DB_PATH:    str = os.path.join(ROOT_PATH, 'db')
DB_PATH:    str = os.path.join(DB_PATH, DB_FILE)


class CRUDModel(metaclass=Singleton):
    def __init__(self, db_log_path: str = DB_PATH, db_name: str = DB_NAME):
        self._table_name: str = db_name
        self.__con: sqlite3.Connection = sqlite3.connect(db_log_path, check_same_thread=False)

    def __create_table(self) -> None:
        self.__con.execute(f"CREATE TABLE IF NOT EXISTS {self._table_name} (currency_code TEXT PRIMARY KEY , rate FLOAT, datetime TEXT)")
        self.__con.commit()
    
    # upsert instead of create and update
    def _upsert(self, currencies: list[dict[str, float, str]]) -> None:
        # Example of currencies format:
        # currency = [
        #               {'char_code': 'USD', 'rate': 90, 'datetime': '02-04-2025 11:10'},
        #               {'char_code': 'EUR', 'rate': 91, 'datetime': '02-04-2025 11:11'},
        #               {'char_code': 'GBP', 'rate': 100, 'datetime': '02-04-2025 11:37'}
        #            ]

        """Upsert data into the table.

        This method does not check if currencies in the list already exist in the table.
        If the currency already exists, its rate and datetime will be updated.

        Args:
            currencies (list[dict[str, float, str]]): A list of dictionaries containing "char_code", 
            "rate", and "datetime" of currencies.
        """
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
    
    def _read(self) -> list[tuple[str, float, str]]:
        """Read all data from the table.

        Returns:
            list[tuple[str, float, str]]: A list of tuples containing "char_code", "rate", and "datetime" of currencies.
        
        Raises:
            sqlite3.Error: If the query fails.
        """
        rates: list[tuple[str, float, str]] = list(
            self.__con.execute(f"SELECT * FROM {self._table_name}")
        )
        return rates
    
    def _delete(self, char_code: str) -> None:
        """Delete a currency from the table.

        Args:
            char_code (str): The currency char code to be deleted.

        Raises:
            sqlite3.Error: If the deletion query fails.
        """
        with self.__con:
            self.__con.execute(f"DELETE FROM {self._table_name} WHERE currency_code = ?", (char_code,))

    @property
    def table_name(self) -> str:
        return self._table_name

    @table_name.setter
    def table_name(self, new_table_name: str) -> None:
        self._table_name = new_table_name
        self.__create_table()
