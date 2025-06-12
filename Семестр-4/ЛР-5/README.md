# Лабораторная работа 5. ООП. ORM

### Задание
На основе предыдущей работы, разработать веб-приложение с использованием фреймворка Flask, в котором будет использоваться ORM для работы с базой данных.

### Описание программы
Веб-приложение на Flask, построенное по MVC-паттерну, которое позволяет пользователю получать и отображать курсы валют (USD, EUR, GBP) с сайта Центробанка РФ. Курсы сохраняются в ORM SQLite-базе данных. Пользователь может запросить новые данные, удалить отдельные валюты и просматривать актуальные значения через веб-интерфейс.

### Структура проекта:
```bash
ЛР-5/
├── app/
|   ├── controllers/
|   │   └── routes.py
|   ├── db/
|   |   └── logtable.db
|   ├── models/
|   |   ├── currency_rates.py
|   |   └── crud_model.py
|   ├── patterns/
|   │   └── patterns.py
|   |── services/
|   |   └── currency_rates.py
|   ├── static/
|   │   └── styles.css
|   ├── templates/
|   │   ├── index.html
|   │   ├── base.html
|   │   └── form.html
|   ├── __init__.py
|   └── database_setup.py
├── db/
|   └── logtable.db
├── config.py
└── run.py
```

# routes.py
```python
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.crud_model import CRUDModel
from app.services.currency_rates import CurrencyRates

bp = Blueprint('main', __name__)


@bp.route('/')
def show():
    db = CRUDModel()
    currency_rates = db._read_all()

    return render_template('form.html', currency_rates=currency_rates)

@bp.route("/fetch", methods=["POST"])
def fetch():
    codes = request.form.get("codes").split()
    
    rates_provider = CurrencyRates()
    del rates_provider.rates
    rates_provider.char_codes = codes
    new_rates = rates_provider.rates

    db = CRUDModel()
    db._upsert(new_rates)

    return redirect(url_for('main.show'))

@bp.route("/delete/<currency_code>", methods=["POST"])
def delete(currency_code):
    db = CRUDModel()
    db._delete(currency_code)

    return redirect(url_for('main.show'))
```

# crud_model.py
```python
import os
import datetime
from app.patterns.patterns import Singleton
from app.models.currency import Currency
from app.database_setup import db


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
```

# currency.py
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.database_setup import db

class Currency(db.Model):
    __tablename__ = 'currencies'

    currency_code = db.Column(db.String, primary_key=True)
    rate = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.String, default=lambda: datetime.utcnow().isoformat())

    def __repr__(self) -> str:
        return f"Currency(currency_code={self.currency_code}, rate={self.rate}, datetime={self.datetime})"
```

# curency_rates.py
```python
import requests
from datetime import datetime
from xml.etree import ElementTree
from app.patterns.patterns import Singleton

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
```

# __init__.py
```python
from flask import Flask
from config import Configuration
from app.database_setup import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)

    with app.app_context():
        from app.models import currency
        db.create_all()

    from app.controllers.routes import bp
    app.register_blueprint(bp)

    return app
```

# database_setup.py
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

# config.py
```python
import os

class Configuration(object):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'db', 'logtable.db')}"
    DEBUG = True
    SERVER_NAME = 'localhost:8080'

```

# run.py
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
```

Анализ:
<br>
Модель ORM реализована через класс Currency, описывающий структуру таблицы в базе данных.

Контроллер (routes.py) обрабатывает маршруты, связывая логику и представление.

Сервисный слой (CurrencyRates) реализует логику получения данных с внешнего API.

ORM (SQLAlchemy) обеспечивает абстракцию над SQL-запросами и упрощает операции чтения, вставки и удаления данных.

В работе с БД используются параметризованные запросы, что предотвращает SQL-инъекции.
