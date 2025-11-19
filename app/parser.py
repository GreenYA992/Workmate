import argparse
import csv
from collections import defaultdict
from typing import Dict, List

from tabulate import tabulate


class DataReader:
    """Класс для чтения данных"""

    @staticmethod
    def read_file(file_path: str) -> List[Dict[str, str]]:
        file = file_path.lower().split(".")[-1]

        if file == "csv":
            return DataReader._read_csv(file_path)
        if file == "json":
            pass
        else:
            raise ValueError(f"Неправильный формат файла {file}")

    @staticmethod
    def _read_csv(file_path: str) -> List[Dict[str, str]]:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]

    @staticmethod
    def _read_json(file_path: str) -> List[Dict[str, str]]:
        pass


class EmpAnalyzer:
    """Анализатор сотрудников"""

    @staticmethod
    def combining_files(file_paths: List[str]) -> List[Dict]:
        """
        Анализируем несколько CSV и возвращаем общий результат
        """
        all_emp = []

        for file_path in file_paths:
            emp = DataReader.read_file(file_path)
            all_emp.extend(emp)

        return all_emp

    @staticmethod
    def calc_stat(employees: List[Dict]) -> List[Dict]:
        """
        Считаем статистику
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
    """Генерируем отчет"""

    @staticmethod
    def report(stats: List[Dict]):
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
    def table_report(stats: List[Dict], file_count: int):
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


def main():
    parser = argparse.ArgumentParser(description="Анализ рейтинга по позициям")
    parser.add_argument("--files", nargs="+", required=True, help="файлы для анализа")
    parser.add_argument(
        "--report",
        nargs="+",
        required=True,
        choices=["performance", "table", "csv"],
        help="тип отчета: performance - списком, table - таблица",
    )
    parser.add_argument("--output", help="Название файла (для сохранения в CSV)")

    args = parser.parse_args()

    all_emp = EmpAnalyzer.combining_files(args.files)
    stats = EmpAnalyzer.calc_stat(all_emp)

    for report_type in args.report:
        if report_type == "table":
            ReportGen.table_report(stats, len(args.files))
        elif report_type == "performance":
            ReportGen.report(stats)
        elif report_type == "csv":
            filename = args.output if args.output else "report.csv"
            ReportGen.save_csv(stats, filename)


if __name__ == "__main__":
    main()

# python parser.py --files ../data_folder/employees1.csv ../data_folder/employees2.csv --report performance
