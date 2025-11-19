import csv
import os
import tempfile
# noinspection PyTypeChecker
from parser import DataReader

import pytest


class TestDataReader:
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
        """Чтение несуществующего файла"""
        with pytest.raises(FileNotFoundError):
            DataReader.read_file("nonexistent_file.csv")

    def test_read_unsupported_format(self):
        """Чтение неподдерживаемого формата"""
        with pytest.raises(ValueError):
            DataReader.read_file("file.txt")
