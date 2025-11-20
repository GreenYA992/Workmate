"""Тесты для модуля DataReader"""

import csv
import os
import tempfile
# noinspection PyTypeChecker
from parser import DataReader

import pytest

class TestDataReader:
    """Тестирование класса DataReader"""

    def test_read_csv_valid_file(self):
        """Тест чтения CSV файла"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(["name", "position", "performance"])
            writer.writerow(["Alex", "Developer", "4.5"])
            writer.writerow(["Maria", "QA", "4.8"])
            temp_path = f.name

        try:
            res = DataReader.read_file(temp_path)
            assert len(res) == 2
            assert res[0]["name"] == "Alex"
            assert res[0]["performance"] == "4.5"
        finally:
            os.unlink(temp_path)

    def test_read_csv_nonexistent_file(self):
        """Тест чтение несуществующего файла"""
        with pytest.raises(FileNotFoundError):
            DataReader.read_file("nonexistent_file.csv")

    def test_read_unsupported_format(self):
        """Тест чтение неподдерживаемого формата"""
        with pytest.raises(ValueError):
            DataReader.read_file("file.txt")

class TestDataReaderErrors:
    """Тесты на обработку ошибок"""
    def test_read_csv_invalid_structure(self):
        """Тест чтение CSV с неправильной структурой"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            w = csv.writer(f)
            w.writerow(['email', 'last_name', 'age'])
            w.writerow(['test1@mail.ru', 'Ivanov', '50'])
            w.writerow(['test2@mail.ru','Petrov','35'])
            temp_path = f.name
        try:
            res = DataReader.read_file(temp_path)
            assert len(res) == 2

            assert 'email' in res[0]
            assert 'last_name' in res[0]
            assert 'age' in res[0]

            assert 'position' not in res[0]
            assert 'performance' not in res[0]
            assert 'name' not in res[0]

        finally:
            os.unlink(temp_path)

    def test_read_csv_empty_file(self):
        """Тест чтение пустого CSV"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write('')
            temp_path = f.name
        try:
            res = DataReader.read_file(temp_path)
            assert res == []
        finally:
            os.unlink(temp_path)
