import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Путь к директории с файлами (можно указать любую папку на компьютере)
DATA_DIR = "data"  # Замените на путь, где лежат ваши CSV файлы


def create_bar_chart(user_count, framework, routes):
    """Создает барчарт с метриками по фреймворкам и пользователям."""
    print(len(routes.items()))
    plt.figure(figsize=(10, 6))
    plt.barh(
        range(len(data_list)),
        [sum(d["values"]) / len(d["values"]) for d in data_list],
        label=[d["framework"] for d in data_list],
    )

    plt.xlabel(metric)
    plt.ylabel("Framework")
    plt.title(f"Average {metric} per Framework (across users)")

    # Добавляет подписи к столбцам с названиями метрик и значениями
    plt.xticks(range(len(data_list)), [d["framework"] for d in data_list])

    # Отображает график барчарта с метриками по фреймворкам и пользователям
    plt.grid(axis="x")
    plt.tight_layout()

    plt.show()


def load_csv_file(file_path):
    """Читает CSV файл и извлекает нужные метрики."""
    try:
        # Читаем весь CSV файл в DataFrame
        df = pd.read_csv(file_path)

        routes = [
            "/cpu",
            "/cpu_fixed",
        ]

        df = df[METRICS_TO_PLOT]

        mask = df["Name"].isin(routes)
        df_filtered = df[mask]

        metrics_dict = {}

        metrics_dict["/cpu"] = df_filtered.loc[df["Name"] == "/cpu"].drop(
            ["Name"], axis=1
        )
        metrics_dict["/cpu_fixed"] = df_filtered.loc[df["Name"] == "/cpu_fixed"].drop(
            ["Name"], axis=1
        )

        # print(metrics_dict)

        return metrics_dict
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return None


# Список метрик для отображения (можно добавить свои)
METRICS_TO_PLOT = [
    "Name",
    "Failure Count",
    "Median Response Time",
    "Average Response Time",
    "Requests/s",
    "Failures/s",
    "50%",
    "90%",
    "99%",
]  # Выберите нужные

# Загружаем данные из всех CSV файлов в текущей директории
all_data = {}

for file_name in os.listdir(DATA_DIR):
    if not file_name.endswith(".csv"):
        continue

    try:
        metrics_dict = load_csv_file(os.path.join(DATA_DIR, file_name))

        # print(metrics_dict)
        # print()

        # Разбиваем имя файла на компоненты (framework, users)
        parts = file_name.replace(".csv", "").split("_")
        framework = parts[0]  # flask, sanic, tornado
        user_count = int(parts[1][:-1])  # 50, 100, 200

        # Сохраняем данные по фреймворку и пользователям
        all_data.setdefault(user_count, {}).setdefault(framework, {})
        for metric_key, metrisc_value in metrics_dict.items():
            all_data[user_count][framework][metric_key] = metrisc_value

        # for user in all_data.keys():
        print(all_data)
        print("\n\n")

    except Exception as e:
        print(f"Ошибка при обработке файла {file_name}: {e}")
        continue


# Создание барчартов для сравнения фреймворков и пользователей
for metric in METRICS_TO_PLOT:
    plt.figure()

    # Создаем список метрик и значений для каждого фреймворка и пользователя
    for user_count, framework_data in all_data.items():
        for framework, routes in framework_data.items():
            # Вызываем функцию для создания барчарта с метриками по фреймворкам и пользователям
            create_bar_chart(user_count, framework, routes)


# plt.show()
