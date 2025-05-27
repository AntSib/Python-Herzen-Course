import os
import datetime
from app.patterns.patterns import Singleton
from app.models.currency import Currency
from app.extensions import db


class CRUDModel(metaclass=Singleton):
    def _upsert(self, currencies: list[dict[str, float, str]]) -> None:
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
        return Currency.query.all()
    
    def _delete(self, currency_code: str) -> None:
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
