import asyncio
import os
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

# =============================================================================
# Утилиты для выполнения CPU-задач
# =============================================================================


def sum_numbers(n: int = 10_000_000) -> tuple[int, float]:
    """
    Выполняет задачу суммирования n чисел (1..n).

    Args:
        n: Количество чисел для суммирования.

    Returns:
        Tuple[sum_result, elapsed_time_sec]
    """
    result = 0
    start_time = time.perf_counter()

    for i in range(n):
        result += i

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    return result, elapsed


def get_cpu_count() -> int:
    """Получает количество процессоров для определения размера пула потоков."""
    return max(1, os.cpu_count() - 1) if hasattr(os, "cpu_count") else 2


# =============================================================================
# Обработчики эндпоинтов
# =============================================================================


class CPURequestHandler(RequestHandler):
    """Обработчик для синхронной CPU-задачи (блокирует поток)."""

    def get(self):
        """Выполняет задачу суммирования синхронно."""
        # Выполняем задачу напрямую в потоке запроса
        result, elapsed = sum_numbers(10_000_000)

        self.set_status(200)
        self.finish(
            json_response(result=result, time_sec=round(elapsed, 3), method="sync")
        )


class CPUFixedRequestHandler(RequestHandler):
    """Обработчик для асинхронной CPU-задачи (использует пул потоков)."""

    async def get(self):
        """Выполняет задачу в отдельном потоке через ThreadPoolExecutor."""
        # Создаем executor с оптимальным количеством рабочих процессов
        n_workers = get_cpu_count()

        with ThreadPoolExecutor(max_workers=n_workers) as pool:
            future = asyncio.get_event_loop().run_in_executor(
                pool, sum_numbers, 10_000_000
            )

            try:
                # Ждем результат с тайм-аутом (600 секунд)
                result, elapsed = await asyncio.wait_for(future, timeout=600)

                self.set_status(200)
                self.finish(
                    json_response(
                        result=result, time_sec=round(elapsed, 3), method="thread"
                    )
                )

            except asyncio.TimeoutError:
                # Если задача превысила тайм-аут - возвращаем ошибку
                error = {
                    "error": "Task timed out",
                    "suggestion": "Increase timeout or use /cpu instead.",
                    "method": "timeout_error",
                }
                self.set_status(504)  # Gateway Timeout
                self.finish(json_response(**error))

            except Exception as e:
                # Обработка других ошибок
                error = {
                    "error": str(e),
                    "suggestion": "Try using /cpu instead of /cpu_fixed",
                    "method": "thread_error",
                }
                self.set_status(500)  # Internal Server Error
                self.finish(json_response(**error))


class CPUFixedProcessHandler(RequestHandler):
    """Обработчик для асинхронной CPU-задачи (использует пул процессов)."""

    async def get(self):
        """Выполняет задачу в отдельном процессе через ProcessPoolExecutor."""
        import multiprocessing as mp

        # Получаем количество процессоров для определения размера пула
        n_workers = max(1, os.cpu_count() - 1)

        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            future = asyncio.get_event_loop().run_in_executor(
                pool, sum_numbers, 10_000_000
            )

            try:
                result, elapsed = await asyncio.wait_for(future, timeout=600)

                self.set_status(200)
                self.finish(
                    json_response(
                        result=result, time_sec=round(elapsed, 3), method="process"
                    )
                )

            except Exception as e:
                error = {
                    "error": str(e),
                    "suggestion": "Try using /cpu instead of /cpu_fixed",
                    "method": "process_error",
                }
                self.set_status(500)
                self.finish(json_response(**error))


def json_response(result=None, time_sec=0.0, **kwargs):
    """Создает JSON-ответ с заданными параметрами."""
    import json

    response_data = {
        "sum": result if "result" in locals() or "result" in kwargs else 19999998,
        "time_sec": time_sec,
        **kwargs,
    }

    return json.dumps(response_data)


# =============================================================================
# Корневой маршрут (API documentation)
# =============================================================================


class IndexHandler(RequestHandler):
    """Корневой маршрут с информацией об API."""

    async def get(self):
        """Возвращает документацию API."""

        import json

        api_doc = {
            "message": "REST API для CPU-задач на Tornado",
            "endpoints": {
                "/cpu": "Выполняет задачу синхронно (блокирует поток)",
                "/cpu_fixed": "Выполняет задачу в отдельном потоке (рекомендуется)",
                "/cpu_process": "Выполняет задачу в отдельном процессе (для мультиядерных CPU)",
            },
            "example_request": """
GET http://localhost:8888/cpu -> {"sum": 19999998, "time_sec": 0.123, "method": "sync"}
GET http://localhost:8888/cpu_fixed -> {"sum": 19999998, "time_sec": 0.145, "method": "thread"}
GET http://localhost:8888/cpu_process -> {"sum": 19999998, "time_sec": 0.234, "method": "process"}
""",
            "performance_notes": {
                "sync": "Блокирует поток Tornado, не подходит для асинхронных клиентов",
                "thread": "Использует ThreadPoolExecutor, работает с CPU-bound задачами эффективно",
                "process": "Использует ProcessPoolExecutor, требует больше памяти но может быть быстрее на мультиядерных CPU",
            },
        }

        self.set_status(200)
        self.finish(json.dumps(api_doc))


# =============================================================================
# Создание и запуск приложения
# =============================================================================

if __name__ == "__main__":
    # Создаем приложение с маршрутами
    application = Application(
        [
            (r"/", IndexHandler),  # Корневой маршрут
            (r"/cpu", CPURequestHandler),  # Синхронный CPU-эндпоинт
            (
                r"/cpu_fixed",
                CPUFixedRequestHandler,
            ),  # Асинхронный CPU-эндпоинт (пул потоков)
        ]
    )

    # Запускаем сервер Tornado на порту 5000
    port = 5000

    print(f"Starting Tornado REST API on http://localhost:{port}")
    print("Endpoints:")
    print(f"  GET /        - API documentation")
    print(f"  GET /cpu     - Sync CPU task (blocking)")
    print(f"  GET /cpu_fixed - Async CPU task (thread pool)")

    application.listen(port)
    IOLoop.current().start()
