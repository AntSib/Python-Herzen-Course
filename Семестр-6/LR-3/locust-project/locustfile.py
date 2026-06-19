import logging

from locust import HttpUser, between, events, task

# Настройка логирования для отладки ошибок
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-5s] %(message)s",
)


class CPUWorker(HttpUser):
    """Основной класс пользователя (работника), который генерирует нагрузку."""

    # По умолчанию, если не передан --host через CLI.
    # Удалите эту строку или замените на реальный хост в продакшене для безопасности.
    host = "http://localhost:5000"
    wait_time = between(0.5, 3)

    def on_start(self):
        """Вызывается один раз при старте симулятора."""
        logging.info("Рабочий узел инициализирован.")

    @task
    def test_cpu_route(self):
        """Тестирует роут /cpu. Вес 1 означает, что запрос генерируется с вероятностью 50%."""
        try:
            self.client.get("/cpu", name="/cpu", timeout=30)
            # В реальном проекте здесь можно добавить проверки кодов ответа
            # если, например, ожидается HTTP 200.
        except Exception as e:
            logging.error(f"Ошибка при запросе к роуту /cpu: {e}", exc_info=True)

    @task
    def test_cpu_fixed_route(self):
        """Тестирует роут /cpu_fixed с весовым коэффициентом 1."""
        try:
            self.client.get("/cpu_fixed", name="/cpu_fixed", timeout=30)
        except Exception as e:
            logging.error(f"Ошибка при запросе к роуту /cpu_fixed: {e}", exc_info=True)


# Глобальные настройки для всех пользователей (опционально)
events.test_start.add_listener(lambda: logging.info("Запуск теста начался"))
events.test_stop.add_listener(lambda: logging.info("Тест завершен"))
