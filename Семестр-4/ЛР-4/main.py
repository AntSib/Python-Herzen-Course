import requests
from xml.etree import ElementTree
from patterns import Singleton

class CurrencyRates(metaclass=Singleton):
    '''
    Class for working with currency rates
    '''
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"
    # CODES = {"USD": "R01235", "EUR": "R01239", "GBP": "R01035"}
    # CODES - словарь отслеживаемых валют
    # удалить CODES

    def __init__(self, char_codes=["USD", "EUR", "GBP"]):
        self._rates:        dict = {}
        self._char_codes:   list = char_codes
        
        self._fetch_rates()

    def _check_char_codes(self) -> bool:
        """
        Check if all char codes are available in given xml

        :return: True if all codes are available, False if not
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
        Fetch currency rates from the given URL and store them in the _rates.

        If the request fails, raise a ConnectionError.
        """
        response = requests.get(self.URL)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            for _valute in tree.findall(".//Valute"):
                # if bool(_valute.find("CharCode")):
                if _valute.find("CharCode").text in self._char_codes:
                    self._rates[_valute.find("CharCode").text] = float(_valute.find("Value").text.replace(",", "."))
        else:
            raise ConnectionError("Не удалось получить данные с сайта ЦБ РФ")


    @property
    def rates(self):
        return self._rates

    @rates.setter
    def rates(self, new_rates):
        self._rates: dict = new_rates

    @rates.deleter
    def rates(self):
        self._rates: dict = {}

    @property
    def char_codes(self):
        return self._char_codes

    @char_codes.setter
    def char_codes(self, new_char_codes):
        self._char_codes: list = new_char_codes
        self._check_char_codes()
        

    @char_codes.deleter
    def char_codes(self):
        self._char_codes: list = []


    # написать код для делитера свойства rates

    # написать код для сеттера атрибута класса CODES, так чтобы мы могли сами
    # переопределять какие валюты мы запрашиваем
    # написать код для геттера, делитера атрибута класса CODES

    # сгенирируйте или напишите и перепроверьте с помощью chatGPT
    # код для делитера атрибута rates






# Пример использования
if __name__ == "__main__":
    rates = CurrencyRates()

    print(rates.rates)  # Вывод всех курсов
    print("Курс USD:", rates.rates.get("USD"))
