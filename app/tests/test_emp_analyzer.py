"""Тесты для модуля EmpAnalyzer"""

import csv
import os
import tempfile
# noinspection PyTypeChecker
from parser import EmpAnalyzer


class TestEmpAnalyzer:
    """Тестирование класса EmpAnalyzer"""

    def test_calc_stat(self):
        """Тест расчета статистики"""
        emp = [
            {"position": "Developer", "performance": "4.5"},
            {"position": "Developer", "performance": "5.0"},
            {"position": "QA", "performance": "4.0"},
        ]

        res = EmpAnalyzer.calc_stat(emp)

        assert len(res) == 2
        dev_stat = next(item for item in res if item["position"] == "Developer")
        assert dev_stat["avg_performance"] == 4.75
        assert dev_stat["employee_count"] == 2
        # проверяем сортировку по убыванию
        assert res[0]["avg_performance"] >= res[1]["avg_performance"]

    def test_calc_empty_data(self):
        """Тест на пустых данных"""
        res = EmpAnalyzer.calc_stat([])
        assert res == []

    def test_calc_single_emp(self):
        """Тест с одним сотрудником"""
        emp = [{"position": "Developer", "performance": "4.5"}]
        res = EmpAnalyzer.calc_stat(emp)

        assert len(res) == 1
        assert res[0]["avg_performance"] == 4.5
        assert res[0]["employee_count"] == 1

    def test_combining_files(self):
        """Тест объединения нескольких файлов"""
        files = []
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            ) as f1:
                writer = csv.writer(f1)
                writer.writerow(["name", "position", "performance"])
                writer.writerow(["Alex", "Developer", "4.5"])
                writer.writerow(["Maria", "Developer", "4.8"])
                files.append(f1.name)

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            ) as f2:
                writer = csv.writer(f2)
                writer.writerow(["name", "position", "performance"])
                writer.writerow(["John", "QA", "5.0"])
                writer.writerow(["Anna", "QA", "4.2"])
                files.append(f2.name)

            res = EmpAnalyzer.combining_files(files)

            assert len(res) == 4  # 2 сотрудника из первого и 2 из второго

            names = [emp["name"] for emp in res]
            assert "Alex" in names
            assert "Maria" in names
            assert "John" in names
            assert "Anna" in names

            positions = [emp["position"] for emp in res]
            assert "Developer" in positions
            assert "QA" in positions

            performances = [emp["performance"] for emp in res]
            assert "4.5" in performances
            assert "4.8" in performances
            assert "5.0" in performances
            assert "4.2" in performances

        finally:
            for file_path in files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
