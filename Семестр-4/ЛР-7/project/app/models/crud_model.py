import os
import datetime
from project.app.patterns.patterns import Singleton
from project.app.models.currency import Currency
from project.app.extensions import db


class CRUDModel(metaclass=Singleton):
    def _upsert(self, currencies: list[dict[str, float, str]]) -> None:
        """
        Add or update the given currencies in the database.

        Args:
            currencies (list[dict[str, float, str]]): A list of dictionaries containing currency data.
        """
        for c in currencies:
            obj = Currency.query.get(c["char_code"])
            if obj:
                obj.rate = c["rate"]
                obj.datetime = c["datetime"]
            else:
                obj = Currency(
                    currency_code=c["char_code"],
                    rate=c["rate"],
                    datetime=c["datetime"]
                )
                db.session.add(obj)
        db.session.commit()
    
    def _read_all(self) -> list[Currency]:
        """
        Get all currencies from the database.

        Returns:
            list[Currency]: A list of all currencies in the database.
        """
        return Currency.query.all()
    
    def _delete(self, currency_code: str) -> None:
        """
        Delete the currency with the given code from the database.

        Args:
            currency_code (str): The code of the currency to delete.
        """
        obj = Currency.query.get(currency_code)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    @property
    def table_name(self) -> str:
        return self._table_name

    @table_name.setter
    def table_name(self, new_table_name: str) -> None:
        self._table_name = new_table_name
        self.__create_table()
