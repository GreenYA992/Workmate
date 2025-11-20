"""Модуль для анализа данных сотрудника и генерации отчетов"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from typing import Dict, List

from tabulate import tabulate


class DataReader:
    """Класс для чтения данных"""

    @staticmethod
    def read_file(file_path: str) -> List[Dict[str, str]]:
        """
        Читает файл и возвращает данные в виде списка словарей.
        Args:
            file_path (str): Путь к файлу
        Returns:
            List[Dict[str, str]]: Данные из файла
        Raise:
            ValueError: Если формат не поддерживается
        """
        file = file_path.lower().split(".")[-1]

        if file == "csv":
            return DataReader._read_csv(file_path)
        if file == "json":
            pass
        else:
            raise ValueError(f"Неправильный формат файла {file}")

    @staticmethod
    def _read_csv(file_path: str) -> List[Dict[str, str]]:
        """
        Читает CSV файл.
        Args:
            file_path (str): Путь к файлу
        Returns:
            List[Dict[str, str]]: Данные из CSV файла
        """
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]

    @staticmethod
    def _read_json(file_path: str) -> List[Dict[str, str]]:
        """
        Читает JSON файл.
        (Метод пропущен, т.к не требуется по заданию)
        Args:
            file_path (str): Путь к файлу
        Returns:
            List[Dict[str, str]]: Данные из JSON файла
        """
        pass


class EmpAnalyzer:
    """Анализатор сотрудников"""

    @staticmethod
    def combining_files(file_paths: List[str]) -> List[Dict]:
        """
        Анализируем несколько файлов.
        Args:
            file_paths (List[str]): Список путей к файлу
        Returns:
            List[Dict[str, str]]: Объединенные данные из файлов
        """
        all_emp = []

        for file_path in file_paths:
            emp = DataReader.read_file(file_path)
            all_emp.extend(emp)

        return all_emp

    @staticmethod
    def calc_stat(employees: List[Dict]) -> List[Dict]:
        """
        Считаем статистику.
        Args:
            employees (List[Dict]): Список данных сотрудников
        Returns:
            List[Dict]: Статистика по должностям
        """
        data = defaultdict(list)

        for emp in employees:
            position = emp["position"]
            performance = float(emp["performance"])
            data[position].append(performance)

        res = []
        for position, performance in data.items():
            avg_performance = sum(performance) / len(performance)
            res.append(
                {
                    "position": position,
                    "avg_performance": round(avg_performance, 2),
                    "employee_count": len(performance),
                }
            )

        res.sort(key=lambda x: x["avg_performance"], reverse=True)
        return res


class ReportGen:
    """Класс генерации отчета"""

    @staticmethod
    def report(stats: List[Dict]):
        """
        Выводим статистику в виде списка.
        Args:
            stats (List[Dict]): Статистика для отчета
        """
        data = []
        for i, stat in enumerate(stats, 1):
            data.append(
                [
                    i,
                    stat["position"],
                    stat["avg_performance"],
                ]
            )
        headers = ["position", "performance"]
        print(
            tabulate(
                data, headers=headers, stralign="left", numalign="right", floatfmt=".2f"
            )
        )

    @staticmethod
    def table_report(stats: List[Dict]):
        """
        Выводим статистику в виде таблицы.
        Args:
            stats (List[Dict]): Статистика для отчета
        """
        data = []
        for stat in stats:
            data.append(
                [
                    stat["position"],
                    stat["avg_performance"],
                    stat["employee_count"],
                ]
            )
        headers = ["Должность", "Рейтинг", "Количество сотрудников"]
        print(tabulate(data, headers=headers, tablefmt="grid", stralign="center"))

    @staticmethod
    def save_csv(stats: List[Dict], filename="report.csv"):
        """
        Сохраняем отчет в CSV файл
        Args:
            stats (List[Dict]): Статистика для сохранения
            filename (str): Имя файла при сохранении
        """
        save_path = (
            "C://Users//Green//OneDrive//Рабочий стол//Обучение//ТЗ//workmate//data_folder//"
            + filename
        )
        with open(save_path, "w", newline="", encoding="utf-8") as f:
            # noinspection PyTypeChecker
            writer = csv.DictWriter(f, fieldnames=["#", "Должность", "Рейтинг"])
            writer.writeheader()
            for i, stat in enumerate(stats, 1):
                writer.writerow(
                    {
                        "#": i,
                        "Должность": stat["position"],
                        "Рейтинг": stat["avg_performance"],
                    }
                )
        print(f"Отчет сохранен в файл: {filename}")


class Validator:
    """Класс для валидации данных"""

    SUPPORTED_EXTENSIONS = ["csv", "json"]
    SUPPORTED_REPORTS = ["performance", "table", "csv"]

    @staticmethod
    def validate_report_type(value):
        """
        Проверка типа отчета
        Args:
            value: Значение для проверки
        Returns:
            str: Проверенное значение
        Raise:
            argparse.ArgumentTypeError: Если формат не поддерживается
        """
        if value not in Validator.SUPPORTED_REPORTS:
            raise argparse.ArgumentTypeError(
                f"\nНеправильный тип отчета {value} !!!. "
                f'\nДоступные типы отчета: {", ".join(Validator.SUPPORTED_REPORTS)}'
            )
        return value

    @staticmethod
    def validate_file_paths(file_paths):
        """
        Проверяет список путей к файлам.
        Args:
            file_paths: Список путей
        Returns:
            List: список valid файлов
        Raise:
            argparse.ArgumentTypeError: если нет valid файлов
        """

        valid_files = []
        missing_files = []
        invalid_format_files = []
        messages = []

        for file_path in file_paths:
            file_ext = file_path.lower().split(".")[-1]
            if file_ext not in Validator.SUPPORTED_EXTENSIONS:
                invalid_format_files.append(file_path)
                continue
            if not os.path.exists(file_path):
                missing_files.append(file_path)
                continue
            valid_files.append(file_path)

        if valid_files:
            messages.append(f"Обработано файлов: {len(valid_files)}")
        if missing_files:
            messages.append(f"Файлы не найдены: {', '.join(missing_files)}")
        if invalid_format_files:
            messages.append(f"Нераспознанный формат: {', '.join(invalid_format_files)}")

        if messages:
            print("\n".join(messages))

        if not valid_files:
            raise argparse.ArgumentTypeError(
                f"Не найдено ни одного файля для обработки. "
                f"Проверьте пути и форматы файлов. "
                f"Поддерживаемые форматы: {', '.join(Validator.SUPPORTED_EXTENSIONS)}"
            )
        return valid_files


def main():
    """Функция для запуска анализатора"""
    parser = argparse.ArgumentParser(description="Анализ рейтинга по позициям")
    parser.add_argument("--files", nargs="+", required=True, help="файлы для анализа")
    parser.add_argument(
        "--report",
        nargs="+",
        required=True,
        type=Validator.validate_report_type,
        help="тип отчета: performance - списком, table - таблица",
    )
    parser.add_argument("--output", help="Название файла (для сохранения в CSV)")

    args = parser.parse_args()

    valid_files = []

    try:
        valid_files = Validator.validate_file_paths(args.files)
    except argparse.ArgumentTypeError as e:
        print(f"Ошибка {e}")
        sys.exit(1)

    all_emp = EmpAnalyzer.combining_files(valid_files)
    stats = EmpAnalyzer.calc_stat(all_emp)

    for report_type in args.report:
        if report_type == "table":
            ReportGen.table_report(stats)
        elif report_type == "performance":
            ReportGen.report(stats)
        elif report_type == "csv":
            filename = args.output if args.output else "report.csv"
            ReportGen.save_csv(stats, filename)


if __name__ == "__main__":
    main()

# python parser.py --files ../data_folder/employees1.csv ../data_folder/employees2.csv --report performance
