"""Тест интеграции приложения"""

import csv
import os
import tempfile
# noinspection PyTypeChecker
from parser import DataReader, EmpAnalyzer, ReportGen

import pytest


class TestIntegration:
    """Интеграционные тесты"""

    def test_workflow(self, capsys):
        """Тест полного workflow"""
        files = []
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            ) as f1:
                writer = csv.writer(f1)
                writer.writerow(["name", "position", "performance"])
                writer.writerow(["Alex", "Developer", "4.5"])
                writer.writerow(["Maria", "QA", "4.8"])
                files.append(f1.name)

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            ) as f2:
                writer = csv.writer(f2)
                writer.writerow(["name", "position", "performance"])
                writer.writerow(["John", "Developer", "5.0"])
                writer.writerow(["Anna", "QA", "4.2"])
                files.append(f2.name)

            emp = EmpAnalyzer.combining_files(files)
            stats = EmpAnalyzer.calc_stat(emp)
            ReportGen.report(stats)

            captured = capsys.readouterr()
            output = captured.out

            assert "Developer" in output
            assert "QA" in output
            assert "4.75" in output
            assert "4.5" in output

        finally:
            for file_path in files:
                if os.path.exists(file_path):
                    os.unlink(file_path)


class TestIntegrationErrors:
    """Интеграционный тест с ошибками"""

    def test_workflow_with_invalid_data(self):
        """Тест workflow с некорректными данными"""
        files = []
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            ) as f:
                w = csv.writer(f)
                w.writerow(["name", "position", "performance"])
                w.writerow(["Alex", "Developer", "Invalid_value"])
                files.append(f.name)

            emp = EmpAnalyzer.combining_files(files)

            with pytest.raises(ValueError):
                EmpAnalyzer.calc_stat(emp)

        finally:
            for file_path in files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
