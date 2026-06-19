import time
from concurrent.futures import ProcessPoolExecutor

from flask import Flask, jsonify

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # Для корректной обработки UTF-8


def sum_numbers(n):
    """Функция для суммирования n чисел"""
    start_time = time.perf_counter()
    total = sum(range(n))
    elapsed = time.perf_counter() - start_time
    return {"sum": total, "time_sec": round(elapsed, 3)}


@app.route("/cpu")
def cpu_endpoint():
    """Выполняет задачу суммирования синхронно (блокирует поток)."""
    result = sum_numbers(10_000_000)
    return jsonify(result), 200


@app.route("/cpu_fixed")
def cpu_fixed_endpoint():
    """Выполняет задачу в отдельном процессе, не блокируя основной поток."""

    # Используем multiprocessing для обхода GIL
    try:
        import os

        # Проверяем наличие доступных ядер CPU (обычно это 1-4)
        n_workers = max(1, os.cpu_count() - 1)

        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            future = pool.submit(sum_numbers, 10_000_000)
            result = future.result(timeout=600)  # Таймаут для безопасности

        return jsonify(result), 200

    except Exception as e:
        error_result = {
            "error": str(e),
            "suggestion": "Попробуйте использовать /cpu вместо /cpu_fixed",
        }
        return jsonify(error_result), 500


@app.route("/")
def index():
    """Корневой маршрут с информацией об API."""
    return jsonify(
        {
            "message": "REST API для CPU-задач",
            "endpoints": {
                "/cpu": "Выполняет задачу синхронно (блокирует поток)",
                "/cpu_fixed": "Выполняет задачу в отдельном процессе (рекомендуется)",
            },
            "example_request": """
        GET http://localhost:5000/cpu -> {"sum": 19999998, "time_sec": ...}
        GET http://localhost:5000/cpu_fixed -> {"sum": 19999998, "time_sec": ...}
        """,
        }
    ), 200


if __name__ == "__main__":
    # Запуск с debug=True для разработки (в продакшене используйте gunicorn/uwsgi)
    app.run(debug=True, host="localhost", port=5000)
