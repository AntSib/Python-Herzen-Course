import requests
from datetime import datetime
from xml.etree import ElementTree
from project.app.patterns.patterns import Singleton

class CurrencyRates(metaclass=Singleton):
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"
    # CODES = {"USD": "R01235", "EUR": "R01239", "GBP": "R01035"}
    # CODES - словарь отслеживаемых валют

    def __init__(self, char_codes=["USD", "EUR", "GBP"]):
        """
        Initialize the class with given char codes

        :param char_codes: list of currency char codes, default is ["USD", "EUR", "GBP"]
        :type char_codes: list[str]
        """
        self._rates:        list = []
        self._char_codes:   list = char_codes
        self._check_char_codes()
        
        self._fetch_rates()

    def _check_char_codes(self) -> None:
        """
        Validates the currency character codes provided during initialization.

        This method sends a GET request to the URL defined in the class to fetch available currency codes.
        It checks if all character codes specified in the _char_codes attribute are present in the available codes
        from the XML response. If any of the specified character codes are not available, a ValueError is raised.

        :raises ValueError: If any specified character codes are not available in the response.
        :raises ConnectionError: If the request to the Central Bank of Russia fails.
        """

        response = requests.get(self.URL)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            available_codes: list = []

            for _code in tree.findall(".//CharCode"):
                if _code.text in self._char_codes:
                    available_codes.append(_code.text)
            
            if not all(set(self._char_codes) & set(available_codes)):
                raise ValueError(f"Недоступные валюты: {set(self._char_codes) - set(available_codes)}")
        else:
            raise ConnectionError("Не удалось получить данные с сайта ЦБ РФ")

    def _fetch_rates(self) -> None:
        """
        Fetch the current currency rates from the Central Bank of Russia.

        This method sends a GET request to the URL defined in the class, parses the XML response,
        and updates the internal list of rates for currencies specified in the _char_codes attribute.
        Each rate is stored as a dictionary containing the currency char code, rate, and the current timestamp.

        :raises ConnectionError: If the request to the Central Bank of Russia fails.
        """
        response = requests.get(self.URL)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            for _valute in tree.findall(".//Valute"):
                # if bool(_valute.find("CharCode")):
                if _valute.find("CharCode").text in self._char_codes:
                    # self._rates[_valute.find("CharCode").text] = float(_valute.find("Value").text.replace(",", "."))
                    self._rates.append({"char_code": _valute.find("CharCode").text, "rate": float(_valute.find("Value").text.replace(",", ".")), "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        else:
            raise ConnectionError("Не удалось получить данные с сайта ЦБ РФ")

    @property
    def rates(self) -> list[dict[str, float, str]]:
        return self._rates

    @rates.deleter
    def rates(self) -> None:
        self._rates: list = []

    @property
    def char_codes(self) -> list[str]:
        return self._char_codes

    @char_codes.setter
    def char_codes(self, new_char_codes) -> None:
        self._char_codes: list = new_char_codes
        self._check_char_codes()
        self._fetch_rates()

    @char_codes.deleter
    def char_codes(self) -> None:
        self._char_codes: list = []
