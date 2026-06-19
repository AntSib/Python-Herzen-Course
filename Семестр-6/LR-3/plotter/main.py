import glob
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Настройка стилистики Matplotlib для красивых графиков по умолчанию
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.figsize"] = [10, 6]  # Стандартный размер графика


class BenchmarkPlotter:
    def __init__(self):
        self.required_columns = {
            "Name": None,
            "Failure Count": None,
            "Median Response Time": None,
            "Average Response Time": None,
            "Requests/s": None,
            "Failures/s": None,
            "50%": None,
            "90%": None,
            "99%": None,
        }

    def extract_columns_from_csv(self, filepath):
        """
        Читает CSV и извлекает только необходимые столбцы.
        Возвращает DataFrame с нужными данными.
        """
        try:
            # Читаем файл, используя 'usecols' для оптимизации скорости чтения
            df = pd.read_csv(
                filepath,
                header=0,  # Заголовки в первой строке (стандарт для локаст)
                usecols=self.required_columns.keys(),
            )

            # Убедимся, что имена колонок совпадают по регистру (иногда бывают странные различия)
            # Приводим названия к нижнему регистру для поиска, если нужно, но обычно у Локаста они четкие.
            # Если в файле колонки названы иначе, потребуется настройка self.required_columns.

            return df
        except FileNotFoundError:
            print(f"  ❌ Файл не найден: {filepath}")
            return None
        except Exception as e:
            print(f"  ❌ Ошибка чтения файла {filepath}: {str(e)}")
            return None

    def plot_single(self, df):
        """
        Рисует график для одного Dataframe.
        Создает основной график и два подграфика (барчарты) для дополнительных метрик.
        """
        if df.empty:
            print("  ⚠️  DataFrame пуст!")
            return

        plt.figure()

        # --- Основной график (Line chart) ---
        # Показываем ключевые метрики производительности относительно времени/запросов
        metrics_main = ["Median Response Time", "Average Response Time", "Requests/s"]

        for col in metrics_main:
            if col in df.columns:
                plt.plot(df.index, df[col], label=col)
            else:
                print(f"  ⚠️  Колонка '{col}' отсутствует в файле.")

        # Подписи осей и легенда
        plt.title("Benchmark Results by Route")
        plt.xlabel("Index (Row)")
        plt.ylabel("Value")
        plt.legend(loc="upper left", fontsize=9)

        # Отрисовка основного графика
        plt.grid(True, linestyle="--", alpha=0.6)

        # --- Подграфик 1: Процентили (50%, 90%, 99%) ---
        ax_percentiles = plt.subplot(211)  # Создаем нижний подграфик в правой части
        metrics_pct = ["50%", "90%", "99%"]

        for col in metrics_pct:
            if col in df.columns:
                # Используем bar для процентилей, так как их обычно сравнивают по величине
                plt.bar(df.index, df[col], alpha=0.8, label=col)

        ax_percentiles.set_title("Percentiles")
        ax_percentiles.legend(loc="upper left", fontsize=8)
        ax_percentiles.grid(True, linestyle=":", alpha=0.4)

        # --- Подграфик 2: Ошибки (Failure Count, Failures/s) ---
        ax_failures = plt.subplot(212)  # Левый нижний подграфик

        metrics_errors = ["Failure Count", "Failures/s"]
        for col in metrics_errors:
            if col in df.columns:
                # Для отрицательных значений или малого объема используем столбчатую диаграмму
                plt.bar(
                    df.index,
                    df[col],
                    alpha=0.8,
                    label=col,
                    color="orange" if col == "Failures/s" else "red",
                )

        ax_failures.set_title("Errors")
        ax_failures.legend(loc="upper left", fontsize=8)
        ax_failures.grid(True, linestyle=":", alpha=0.4)

        plt.tight_layout()  # Адаптирует подложку под элементы графика

        # Имя файла для сохранения
        filename = Path(df.iloc[0]["Name"]) if any(df["Name"]) else "unknown"
        save_name = f"{filename}.png".strip("\\")

        # Сохраняем график
        plt.savefig(save_name)
        print(f"  ✅ График сохранен: {save_name}")

        plt.show()


def run_analysis():
    plotter = BenchmarkPlotter()

    # 1. Формируем список всех возможных имен файлов согласно ТЗ
    frameworks = ["flask", "sanic", "tornado"]
    users = [50, 100, 200]

    file_patterns = []
    for fw in frameworks:
        for u in users:
            # Формируем строку по шаблону: framework_usersu_3m.csv
            # Учет регистра букв (обычно Локаст пишет FLASK или flask, в ТЗ строчные)
            filename = f"{fw}_{u}u_3m.csv"
            file_patterns.append(filename)

    print("Начинаем поиск файлов и отрисовку графиков...")

    # 2. Ищем файлы на диске (поиск нечувствителен к регистру, если имена совпадают по смыслу)
    found_files = []

    # Если файлы в текущей папке, ищем их прямо там
    base_dir = "data"
    for pattern in file_patterns:
        files = glob.glob(os.path.join(base_dir, f"*{pattern}*")) + glob.glob(
            os.path.join(base_dir, f"*{pattern}")
        )

        # Уточненный поиск для точного совпадения имени (в зависимости от регистра в реальных файлах)
        exact_matches = glob.glob(
            os.path.join(base_dir, "**", pattern.replace(" ", "")), recursive=True
        )

        for f in exact_matches:
            if os.path.isfile(f):
                found_files.append(f)

    if not found_files:
        # Если точное совпадение не нашлось, пробуем вариации регистра (наиболее частая проблема)
        print(
            "\n⚠️  Точные файлы с нижним регистром не найдены. Пробуем варианты регистра имен..."
        )
        for pattern in file_patterns:
            # Генерируем все возможные комбинации регистра для поиска
            variants = []
            for char in list(pattern):
                upper_variants = (
                    [s.upper() for s in file_patterns]
                    + [s.capitalize() for s in file_patterns]
                    + [s.lower() for s in file_patterns]
                )

                # Простой хак: попробуем найти файлы, содержащие подстроку (не чувствительно к регистру)
                # Но лучше использовать glob с маскировкой если точное имя неизвестно
                pass

            # Упрощенный поиск для "грязных" данных Локаста
            search_patterns = []
            for fp in file_patterns:
                # Добавляем верхний регистр к имени файла как альтернативу (часто бывает FLASK_50u_3m.csv)
                upper_fp = fp.upper()
                mixed_fws = ["Flask", "Sanic", "Tornado"]
                for fw in mixed_fws:
                    mixed_fp = (
                        f"{fw}_{fp.split('_')[1]}{fp.split('_')[2]}"  # Примерной микс
                    )

                if not any(p in found_files for p in [fp, upper_fp]):
                    # Пытаемся найти файл по подстроке для коррекции регистра
                    potential_match = glob.glob(
                        os.path.join(base_dir, "**", fp.upper() or "*"), recursive=True
                    )
                    if potential_match:
                        found_files.extend(potential_match)

    # Убираем дубликаты
    found_files = sorted(list(set(found_files)))

    if not found_files:
        print("❌ Файлы не найдены в текущей директории или поддиректориях.")
        print("Проверьте, что файлы называются точно так:\n flask_50u_3m.csv, etc.")
        return

    print(f"Найдено файлов для анализа: {len(found_files)}")

    # 3. Цикл обработки каждого найденного файла
    for filepath in found_files:
        print(f"\n--- Обработка файла: {Path(filepath).name} ---")

        df = plotter.extract_columns_from_csv(filepath)

        if df is not None and not df.empty:
            plotter.plot_single(df)


if __name__ == "__main__":
    run_analysis()
import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Настройка стиля для приятного отображения графиков
plt.style.use("seaborn-v0_8-deep")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [
    "DejaVu Sans",
    "Arial",
    "Helvetica",
]  # Попытка выбрать системные шрифты


def plot_locust_data(directory="data"):
    # Путь к шаблонам файлов
    pattern = os.path.join(directory, "*_u_3m.csv")

    # Поиск всех подходящих файлов
    files = glob.glob(pattern)

    if not files:
        print(
            f"Ошибка: Найдено 0 файлов по паттерну {pattern} в директории {directory}."
        )
        return

    print(f"Найдено {len(files)} файлов для обработки.")

    for file_path in files:
        try:
            # Чтение CSV файла
            df = pd.read_csv(file_path)

            # Нам интересны строки с индексами 1 и 2 (в 0-индексированном pandas это index 1 и 2)
            # Первая строка (index 0) - заголовки, пропускаем.
            rows_to_plot_indices = [1, 2]

            target_rows_data = {}

            for idx in rows_to_plot_indices:
                if idx < len(df):
                    row = df.iloc[idx]
                    # Создаем копию строки, чтобы не портить оригинал
                    target_rows_data[f"row_{idx + 1}"] = row

            # Определяем колонки с данными.
            # Идем по файлу и берем названия колонок, если в имени колонки есть текст (не пустая строка)
            metric_names = []
            for col in df.columns:
                name = str(col).strip()
                if name and not pd.isna(name):
                    metric_names.append(name)

            # Проверка: у нас должны быть данные для всех найденных метрик
            if len(metric_names) < 3:
                print(
                    f"Предупреждение по файлу {file_path}: Не удалось найти достаточно числовых колонок. Пропускаем."
                )
                continue

            # Функция для создания графика одной строки данных
            def create_subplot(ax, row_data, title_suffix):
                x = metric_names
                y = [
                    row_data[col] for col in metric_names if pd.notna(row_data.get(col))
                ]

                # Фильтруем null значения из y перед созданием бара, но сохраняем порядок
                clean_x = [x[i] for i in range(len(x)) if pd.notna(y[i])]
                clean_y = [y[i] for i in range(len(y)) if pd.notna(y[i])]

                if not clean_y:
                    ax.text(
                        0.5,
                        1.0,
                        "Нет данных",
                        ha="center",
                        va="bottom",
                        transform=ax.transData,
                    )
                    return

                # Отрисовка барчарта
                bars = ax.bar(
                    clean_x,
                    clean_y,
                    width=0.8,
                    color="#2ca02c" if "Count" in x[0] else "#ff7f0e",
                )

                # Форматирование заголовка подграфика (Framework и Users из имени файла)
                filename = os.path.basename(file_path).replace(".csv", "")
                ax.set_title(
                    f"{title_suffix}\n{filename}", fontsize=12, fontweight="bold"
                )

                ax.set_xlabel("Metric Name", fontsize=10)
                ax.set_ylabel("Value", fontsize=10)
                ax.grid(axis="y", linestyle="--", alpha=0.3)

                # Отформатируем подписи осей X, чтобы не накладывались слишком сильно
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

            # Создание фигуры с двумя подграфиками (вертикально)
            fig, axs = plt.subplots(2, 1, figsize=(14, 10))

            filename_short = (
                os.path.basename(file_path).replace(".csv", "").replace(" ", "_")
            )

            # Заголовки для подграфиков:
            # Строка 2 файла -> Title A
            # Строка 3 файла -> Title B
            row_titles = [f"Locust Metrics (Row 2)", f"Locust Metrics (Row 3)"]

            # Рисуем верхний график (Строка 1 из файлов, индекс 1 в pandas)
            create_subplot(axs[0], target_rows_data["row_2"], row_titles[0])

            # Рисуем нижний график (Строка 2 из файлов, индекс 2 в pandas)
            create_subplot(axs[1], target_rows_data["row_3"], row_titles[1])

            plt.suptitle(
                f"Load Test Results: {filename_short}",
                fontsize=16,
                fontweight="bold",
                y=0.98,
            )

            # Сохранение файла с графиком (исключаем расширение csv из имени png)
            base_name = os.path.splitext(file_path)[0]
            output_filename = f"{base_name}.png"
            plt.savefig(output_filename, dpi=300, bbox_inches="tight")
            print(f"График сохранен в: {output_filename}")

            # Отображение
            plt.show()

        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {str(e)}")
            continue


if __name__ == "__main__":
    plot_locust_data(directory="data")
