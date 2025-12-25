import warnings
from datetime import datetime
from xml.etree import ElementTree as ET

import requests


class CurrencyRates:
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"

    def __init__(self, char_codes: list[str]):
        """
        Initialize the class with given char codes.

        Args:
            char_codes: list of currency char codes, default is ["USD", "EUR", "GBP"]

        """
        self.char_codes = set(char_codes)

    def fetch(self) -> list[dict]:
        # Google style docstring
        """
        Fetch the current currency rates from the Central Bank of Russia.

        This method sends a GET request to the URL defined in the class, parses the XML response,
        and returns a list of dictionaries containing the currency char code, rate, and the current timestamp.

        If the request to the Central Bank of Russia fails, a ConnectionError is raised.

        If any of the specified character codes are not available in the response, a warning is raised.

        Returns:
            list: A list of dictionaries containing the currency char code, rate, and the current timestamp.

        """
        if not self.char_codes:
            return []

        response = requests.get(self.URL, timeout=5)
        if response.status_code != 200:
            raise ConnectionError("Не удалось получить данные с сайта ЦБ РФ")

        tree = ET.fromstring(response.content)

        available_rates = {}
        for valute in tree.findall(".//Valute"):
            code = valute.findtext("CharCode")
            if code in self.char_codes:
                available_rates[code] = {
                    "char_code": code,
                    "rate": float(valute.findtext("Value").replace(",", ".")),
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

        missing = self.char_codes - available_rates.keys()
        if missing:
            warnings.warn(f"\nВалюты {', '.join(missing)} не найдены")  # noqa: B028

        return list(available_rates.values())
