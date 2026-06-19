import time
from concurrent.futures import ThreadPoolExecutor

from sanic import Sanic
from sanic.response import json as sanic_json


def sum_numbers(n: int = 10_000_000) -> tuple[int, float]:
    """Выполняет суммирование чисел и возвращает результат + время выполнения."""
    start = time.perf_counter()
    result = sum(i for i in range(n))
    elapsed = time.perf_counter() - start
    return result, elapsed


async def index_endpoint(request):
    """Корневой маршрут с информацией об API."""
    return sanic_json(
        {
            "message": "REST API для CPU-задач на Sanic",
            "endpoints": {
                "/cpu": "Выполняет задачу синхронно (блокирует поток)",
                "/cpu_fixed": "Выполняет задачу в отдельном потоке (рекомендуется)",
            },
            "example_request": """
    GET http://localhost:8000/cpu -> {"sum": 19999998, "time_sec": ...}
    GET http://localhost:8000/cpu_fixed -> {"sum": 19999998, "time_sec": ...}
    """,
        },
    )


async def cpu_endpoint(request):
    """Выполняет задачу суммирования синхронно (блокирует поток)."""
    result, elapsed = sum_numbers(10_000_000)

    return sanic_json(
        {"sum": result, "time_sec": round(elapsed, 3), "method": "sync"}, status=200
    )


async def cpu_fixed_endpoint(request):
    """Выполняет задачу в отдельном потоке, не блокируя основной поток."""
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(sum_numbers, 10_000_000)

        try:
            result, elapsed = future.result(timeout=600)

            return sanic_json(
                {"sum": result, "time_sec": round(elapsed, 3), "method": "thread"},
                status=200,
            )

        except Exception as e:
            error_result = {
                "error": str(e),
                "suggestion": "Попробуйте использовать /cpu вместо /cpu_fixed",
                "method": "thread_error",
            }
            return sanic_json(error_result, status=500)


app = Sanic("CPU-API")

app.add_route(index_endpoint, "/", methods=["GET"])
app.add_route(cpu_endpoint, "/cpu", methods=["GET"])
app.add_route(cpu_fixed_endpoint, "/cpu_fixed", methods=["GET"])


if __name__ == "__main__":
    app.run(
        debug=True,
        host="localhost",
        port=5000,
        single_process=True,
        access_log=False,
    )
