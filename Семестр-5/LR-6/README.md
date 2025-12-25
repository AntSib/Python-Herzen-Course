# Лабораторная работа 6. Использование шаблона «Наблюдатель»

**Задание**: Создать полный глоссарий употребляемых терминов по определённой области и спроектировать доступ к нему в виде Web API в Docker-контейнере.

### Структура проекта

```
project/
├─ app/
│ ├─ controllers/
│ │ └─ routes.py
│ ├─ models/
│ │ ├─ crud.py
│ │ └─ currency_model.py
│ ├─ observers/
│ │ └─ rates_subject.py
│ ├─ patterns/
│ │ └─ singleton.py
│ ├─ services/
│ │ └─ currency_rates.py
│ ├─ sockerts/
│ │ └─ events.py
│ ├─ static/
│ │ ├─ currency_ws.js
│ │ └─ style.css
│ ├─ templates/
│ │ ├─ base.html
│ │ └─ form.html
│ ├─ __init__.py
│ └─ database_setup.py
├─ db/
│ └─ logtable.db
├─ config.py
└─ main.py
```

Часть новых файлов:
```python 
# app/observers/rates_subject.py
import threading
from collections import defaultdict

from app.models.crud import DBManager
from app.services.currency_rates import CurrencyRates


class RatesSubject:
    UPDATE_INTERVAL = 10  # seconds

    def __init__(self, app, socketio):
        """
        Initializes the RatesSubject with the given app and socketio instance.

        Args:
            app (Flask): The Flask app instance.
            socketio (SocketIO): The SocketIO instance.

        """
        self.app = app
        self.socketio = socketio

        self._subscriptions: dict[str, set[str]] = defaultdict(set)

        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def subscribe(self, sid: str, codes: list[str]) -> None:
        """
        Subscribe the given sid to the given list of currency codes.

        This method will update the set of codes for the given sid.

        Args:
            sid (str): The sid to subscribe.
            codes (list[str]): The list of currency codes to subscribe to.

        """
        self._subscriptions[sid].update(codes)

    def unsubscribe(self, sid: str, code: str) -> None:
        """
        Unsubscribe the given sid from the given currency code.

        If the sid no longer has any subscribed codes, the entry is removed from the subscriptions dict.

        Args:
            sid (str): The sid to unsubscribe.
            code (str): The currency code to unsubscribe from.

        """
        self._subscriptions[sid].discard(code)
        if not self._subscriptions[sid]:
            del self._subscriptions[sid]

    def unsubscribe_all(self, sid: str) -> None:
        """
        Unsubscribe the given sid from all currency codes.

        If the sid no longer has any subscribed codes, the entry is removed from the subscriptions dict.

        Args:
            sid (str): The sid to unsubscribe from all currency codes.

        """
        self._subscriptions.pop(sid, None)

    def _active_codes(self) -> set[str]:
        """
        Returns a set of all active currency codes.

        A currency code is considered active if there is at least one subscription to it.

        Returns:
            set[str]: A set of all active currency codes.

        """
        result = set()
        for codes in self._subscriptions.values():
            result.update(codes)
        return result

    def start(self) -> None:
        """Starts the timer to periodically update the currency rates."""
        if self._timer is None:
            self._schedule()

    def _schedule(self) -> None:
        """
        Schedules the currency rates to be updated periodically.

        This method creates a Timer object that will call the _update method every self.UPDATE_INTERVAL seconds.
        The Timer object is set to run as a daemon thread, so it will exit when the main thread exits.
        The Timer object is then started.
        """
        self._timer = threading.Timer(self.UPDATE_INTERVAL, self._update)
        self._timer.daemon = True
        self._timer.start()

    def _update(self) -> None:
        """
        Periodically updates the currency rates and notifies the subscribed clients of any changes.

        This method is called by a Timer object every self.UPDATE_INTERVAL seconds.
        It checks if there are any active subscriptions and if so, it fetches the current rates of the active currencies.
        It then checks if there have been any changes in the rates and if so, it notifies the subscribed clients of the changes.
        Finally, it schedules the next update.
        """
        if not self._lock.acquire(blocking=False):
            return

        try:
            with self.app.app_context():
                print("Updating rates...")
                print(f"Active subscriptions: {list(self._subscriptions)}")

                codes = self._active_codes()
                if not codes:
                    return

                provider = CurrencyRates(list(codes))
                new_rates = provider.fetch()

                db = DBManager()
                changed_rates = []

                for rate in new_rates:
                    old = db.get_by_code(rate["char_code"])
                    if old is None or float(old.rate) != rate["rate"]:
                        db.upsert([rate])
                        changed_rates.append(rate)

                if changed_rates:
                    self._notify_clients(changed_rates)

        finally:
            self._lock.release()
            self._schedule()

    def _notify_clients(self, rates: list[dict]) -> None:
        """
        Notify all subscribed clients of the given rate changes.

        This method takes a list of dictionaries, where each dictionary contains the
        currency char code, rate, and the current timestamp. It then checks which
        clients have subscribed to each of the active currencies and notifies them
        of the changes in the rates.

        Args:
            rates (list[dict]): A list of dictionaries containing the currency char code,
                rate, and the current timestamp.

        """
        for sid, codes in self._subscriptions.items():
            personal_updates = [r for r in rates if r["char_code"] in codes]
            if personal_updates:
                self.socketio.emit(
                    "rates_update",
                    personal_updates,
                    room=sid,
                )
```

```python
# app/sockets/events.py
from flask import current_app, request
from flask_socketio import emit


def register_socket_events(socketio):
    """
    Registers socket events for given socketio instance.

    Listens for "connect", "subscribe", "unsubscribe" and "disconnect" events.

    Emits "client_id" event with the client's sid upon connection.
    Subscribes given codes to the RatesSubject upon subscription.
    Unsubscribes given code from the RatesSubject upon unsubscription.
    Unsubscribes all codes from the RatesSubject upon disconnection.
    """

    @socketio.on("connect")
    def connect():
        emit("client_id", {"client_id": request.sid})

    @socketio.on("subscribe")
    def subscribe(data):
        codes = data.get("codes", [])
        subject = current_app.extensions["rates_subject"]
        subject.subscribe(request.sid, codes)

    @socketio.on("unsubscribe")
    def unsubscribe(data):
        code = data.get("code")
        subject = current_app.extensions["rates_subject"]
        subject.unsubscribe(request.sid, code)

    @socketio.on("disconnect")
    def disconnect():
        subject = current_app.extensions["rates_subject"]
        subject.unsubscribe_all(request.sid)
```

```javascript
// app/sockets/index.js
const socket = io();
const table = document.getElementById("rates-table");
const form = document.getElementById("codes-form");
const input = document.getElementById("codes-input");

const subscribedCodes = new Set();

/* === CONNECT === */

socket.on("client_id", data => {
    document.getElementById("client-id").textContent = data.client_id;
});

/* === UPDATES FROM SERVER === */

socket.on("rates_update", rates => {
    rates.forEach(rate => {
        if (subscribedCodes.has(rate.char_code)) {
            updateRow(rate);
        }
    });
});

/* === FORM SUBMIT === */

form.addEventListener("submit", e => {
    e.preventDefault();

    const codes = input.value
        .replace(/,/g, '')
        .toUpperCase()
        .split(/\s+/)
        .filter(Boolean);

    if (!codes.length) return;

    codes.forEach(c => subscribedCodes.add(c));
    socket.emit("subscribe", { codes });

    fetch("/fetch", {
        method: "POST",
        body: new URLSearchParams({ codes: codes.join(" ") })
    })
    .then(r => r.json())
    .then(data => {
        data.rates.forEach(updateRow);
    });
    input.value = "";
});

/* === TABLE BUILDERS === */

function updateRow(rate) {
    let row = document.getElementById(rate.char_code);

    if (!row) {
        row = document.createElement("tr");
        row.id = rate.char_code;
        row.innerHTML = `
            <td>${rate.char_code}</td>
            <td class="rate"></td>
            <td class="date"></td>
            <td>
              <button data-code="${rate.char_code}">Удалить</button>
            </td>
        `;
        row.querySelector("button").onclick = removeRow;
        table.appendChild(row);
    }

    row.querySelector(".rate").textContent = rate.rate;
    row.querySelector(".date").textContent = rate.datetime;
}

function removeRow(e) {
    const code = e.target.dataset.code;
    subscribedCodes.delete(code);
    document.getElementById(code)?.remove();
    socket.emit("unsubscribe", { code });
}

```


## Описание проделанной работы

Был переработан класс получения курсов валют:
Убран паттерн Singleton и переработан в stateless, благодаря чему данные не хранятся внутри экземпляра между вызовами. Каждый запрос создаёт краткоживущий объект.

Это позволило избежать скрытого состояния и безопасно использовать сервис в потоках и таймерах.

Добавлен компонент RatesSubject, выполняющий роль наблюдаемого объекта:
Его функции:
* хранить список подписчиков (Socket.IO-клиентов);
* запускать периодическое обновление курсов;
* получать актуальные данные из БД (источник истины);
* рассылать обновления подписанным клиентам.

Особенности:
* CurrencyRates используется только для обновления БД;
* сам Subject не хранит состояние курсов.

### Реализация per-client подписок
Каждый клиент:
* подписывается только на запрошенные валюты;
* может удалить валюту только у себя (локально);
* не влияет на данные в БД и других клиентов.

Подписка реализована через:
* flask-socketio;
* namespace;
* привязку валют к sid клиента.

Вся логика работы с интерфейсом была вынесена в static/currency_ws.js:
* отправка запросов на добавление валют;
* управление отображаемыми строками таблицы;
* предотвращение дублирования данных;
* обработка Socket.IO-сообщений.

HTML-шаблон теперь отвечает только за разметку.

### Анализ
В результате внедрения паттерна Observer и реализации подписок приложение получило расширенный функционал с автоматическим обновлением курсов и поддержкой индивидуальных подписок пользователей. Архитектура стала более устойчивой, предсказуемой и соответствующей принципам чистого проектирования.
