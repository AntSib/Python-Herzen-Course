# Лабораторная работа 4. ООП. Курсы валют

### Задание

https://cbr.ru/development/SXML/
<br>
Класс, который при создании объекта этого класса отправляет запрос к сайту ЦБ и сохраняет курсы доллара, евро и фунта в словаре с ключами. Например: USD, EUR, GBP.

Требования:
<br>
Список, который передает пользователь хранится в self._char_codes словарь отслеживаемых валют CODES хранился в объекта класса CurrencyRates при создании объекта мы задаем "человеческие" коды валют (например, USD, EUR, GBP) наш объект имеет метод, который "разрешает" имена валют и запрашивает текущий курс с помощью метода _fetch_rates.
Для переменной _rates у нас есть геттер, однако для переменной self._char_code у нас есть getter, setter, deleter, причем для сеттера у нас есть какая-то проверка на валидность значений валют, если значения валидны, то отправляем запрос к АПИ для получения новых значений валют.

Применить к классу CurrencyRates декоратор singleton.

Написать почему способ с использованием декоратора-функции плох,
написать какой правильный способ создания синглтона есть и его использовать в работе.

Использовать в коде здесь правильный шаблон "Одиночка" (с использованием метаклассов)

Создать базу данных и реализовать CRUD: добавление значения валют, считывание (select), обновление, удаление. Использовать параметризованные запросы для добавления и считывания.

Придумать и сформулировать подход для реализации MVC-паттерна для данной задачи (т.е. каким образом и где должен размещаться функционал для получения значения валют, где должен располагаться функционал для добавления в БД значения валют, а где должно отображаться значения валют (компонент View).

### Описание программы
Веб-приложение на Flask, построенное по MVC-паттерну, которое позволяет пользователю получать и отображать курсы валют (USD, EUR, GBP) с сайта Центробанка РФ. Курсы сохраняются в SQLite-базе данных. Пользователь может запросить новые данные, удалить отдельные валюты и просматривать актуальные значения через веб-интерфейс.

### Структура проекта:
app/
├── controllers/
│   └── routes.py
├── db/
|   └── logtable.db
├── models/
|   ├── currency_rates.py
|   └── crud_model.py
├── patterns/
│   └── patterns.py
├── static/
│   └── styles.css
├── templates/
│   ├── index.html
│   ├── base.html
│   └── form.html
├── app.py
└── config.py

# routes.py
```python
from flask import Blueprint, render_template, request, redirect, url_for
from models.crud_model import CRUDModel
from models.currency_rates import CurrencyRates

bp = Blueprint('main', __name__)


@bp.route('/')
def show():
    db = CRUDModel()
    currency_rates = db._read()

    return render_template('form.html', currency_rates=currency_rates)

@bp.route("/fetch", methods=["POST"])
def fetch():
    db = CRUDModel()
    rates_provider = CurrencyRates()

    codes = request.form.get("codes").split()
    del rates_provider.rates
    rates_provider.char_codes = codes
    fresh_rates = rates_provider.rates
    
    db._upsert(fresh_rates)

    return redirect(url_for('main.show'))

@bp.route("/delete/<code>", methods=["POST"])
def delete(code):
    db = CRUDModel()
    db._delete(code)

    return redirect(url_for('main.show'))
```

# currency_rates.py
```python
import requests
from datetime import datetime
from xml.etree import ElementTree
from patterns.patterns import Singleton

class CurrencyRates(metaclass=Singleton):
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"
    # CODES = {"USD": "R01235", "EUR": "R01239", "GBP": "R01035"}

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
                if _valute.find("CharCode").text in self._char_codes:
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
```

# crud_model.py
```python
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
        self.__create_table()

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
```

# patterns.py
```python
# Usage of singleton decorator
# By use of decorator, class will be converted to function, which is not assessible for OOP concepts
def singleton(cls: type) -> callable:
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance


# Usage of metaclass as singleton
# By use of metaclass, class can be inherited from this metaclass, stayning as a class
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
```

# app.py
```python
from flask import Flask
from config import Configuration
from controllers.routes import bp

app = Flask(__name__)

app.register_blueprint(bp)
app.config.from_object(Configuration)

if __name__ == '__main__':
    app.run()
```

Анализ:
<br>
ООП (Объектно-Ориентированное Программирование):
    Применяются инкапсуляция, свойства с геттерами/сеттерами/делетерами, а также соблюдён принцип SRP (Single Responsibility Principle): CurrencyRates отвечает за загрузку данных, CRUDModel — за работу с БД.

Шаблон Singleton:
    Использован корректный способ реализации через метакласс Singleton, который сохраняет возможность использовать ООП-принципы (в отличие от декоратора, который превращает класс в функцию).

Работа с SQLite:
    Выполняется через параметризованные запросы (предотвращение SQL-инъекций). Используется UPSERT, что упрощает обновление курсов без лишней логики.


MVC-подход:
* Model: CurrencyRates (работа с API) и CRUDModel (работа с БД).
* Controller: routes.py, где обрабатываются маршруты, логика запроса и обновления данных.
* View: шаблоны в templates/, где отображаются данные для пользователя.
