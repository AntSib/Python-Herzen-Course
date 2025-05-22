"""Глоссарий должен поддерживать следующие операции:
    Получение списка всех терминов.
    Получение информации о конкретном термине по ключевому слову.
    Добавление нового термина с описанием.
    Обновление существующего термина.
    Удаление термина из глоссария.
    У вас должен применяться Pydantic для валидации входных данных и формирования схем.
    Будет плюсом, если вы:
    - найдете и используете по назначению инструмент для автоматической генерации статической документации
    с помощью встроенной OpenAPI-спецификации FastAPI;
    - реализуйте решение в виде контейнера (Dockerfile) или реализуйте решение с помощью Docker Compose;
    - используете для хранения данных  SQLite (или другую легковесную БД);
    - обеспечите автоматическую миграцию структуры данных при старте приложения.
"""

from http.client import HTTPException
from typing import Union, Dict

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Valute(BaseModel):
    name: str
    time_n_date: Union[str, None] = ""
    value: float


class Term(BaseModel):
    description: str


glossary: Dict[str, Term] = {
    'REST': Term(
        description='«передача репрезентативного состояния» или «передача „самоописываемого“ состояния») — архитектурный стиль взаимодействия компонентов распределённого приложения в сети.'),
    'RPC': Term(
        description='Удалённый вызов процедур (Remote Procedure Call, RPC) — это механизм, который позволяет одной программе вызывать процедуры или функции другой программы, расположенной на другом компьютере в сети.')
}


@app.get("/terms")
def get_all_terms():
    return glossary


@app.get("/terms/{term}")
def get_term(term: str):
    if term not in glossary:
        raise HTTPException(status_code=404, detail="Term not found")
    return glossary.get(term, "term not found")


@app.post("/terms/{term}", response_model=Dict[str, Term])
def post_term(term: str, term_data: Term):
    if term in glossary:
        raise HTTPException(status_code=400, detail="Term already exists!")
    glossary[term] = term_data
    return {term: term_data}


@app.put("/terms/{term}", response_model=Dict[str, Term])
def change_term(term: str, term_data: Term):
    if term not in glossary:
        raise HTTPException(status_code=400, detail="Term not found!")
    glossary[term] = term_data
    return {term: term_data}


@app.delete("/terms/{term}")
def delete_term(term: str):
    if term not in glossary:
        raise HTTPException(status_code=404, detail="Term not found!")
    del glossary[term]
    return {"result": "deleted successfully"}


@app.get("/")
def read_root():
    return "Root page"


# Создать endpoint, в котором возвращается имя и текущая дата и время по-русски
# {"author": "Nick", "datetime": "Среда, 16.04.2025 12:35"}
@app.get('/author')
def read_about():
    from datetime import datetime
    import locale
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    today = datetime.now().strftime("%A, %d.%m.%Y, %H:%M").title()

    return {'author': "Nick", "datetime": f'{today}'}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/valute/{valute_id}")
def read_valute(valute_id: str):
    return {"valute_id": valute_id}


@app.put("/valute/{valute_id}")
def update_valute(valute_id: str, _valute: Valute):
    # _valute.name = valute_id
    # _valute.value = 90
    return {"valute_name": _valute.name, "valute_val": _valute.value}


# favicon
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return None

