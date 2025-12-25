from app.database_setup import db
from app.models.currency_model import Currency
from app.patterns.singleton import Singleton


class DBManager(metaclass=Singleton):
    def upsert(self, currencies: list[dict[str, float, str]]) -> None:
        """
        Upsert data into the table.

        This method does not check if currencies in the list already exist in the table.
        If the currency already exists, its rate and datetime will be updated.

        Args:
            currencies (list[dict[str, float, str]]): A list of dictionaries containing "char_code", "rate", and "datetime" of currencies.

        Raises:
            sqlite3.Error: If the query fails.

        """
        for currency in currencies:
            obj = Currency.query.get(currency["char_code"])
            if obj:
                obj.rate = currency["rate"]
                obj.datetime = currency["datetime"]
            else:
                obj = Currency(
                    currency_code=currency["char_code"],
                    rate=currency["rate"],
                    datetime=currency["datetime"],
                )
                db.session.add(obj)
        db.session.commit()

    def get_all(self) -> list[Currency]:
        """
        Read all data from the table.

        Returns:
            list[Currency]: A list of objects containing "char_code", "rate", and "datetime" of currencies.

        Raises:
            sqlite3.Error: If the query fails.

        """
        return Currency.query.all()

    def get_by_code(self, currency_code: str) -> Currency:
        """
        Read a currency from the table by its char code.

        Args:
            currency_code (str): The currency char code to be read.

        Returns:
            Currency: An object containing "char_code", "rate", and "datetime" of the currency.

        Raises:
            sqlite3.Error: If the query fails.

        """
        return Currency.query.get(currency_code)

    def delete(self, currency_code: str) -> None:
        """
        Delete a currency from the table by its char code.

        Args:
            currency_code (str): The currency char code to be deleted.

        Raises:
            sqlite3.Error: If the deletion query fails.

        """
        obj = self.get_by_code(currency_code)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    @property
    def table_name(self) -> str:
        """
        The name of the database table used by the model.

        Returns:
            str: The name of the database table.

        """
        return self._table_name
