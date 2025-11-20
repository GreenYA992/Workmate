"""Тесты для модуля Validator"""
import argparse

import pytest
import tempfile
import os
from parser import Validator

class TestValidator:
    """Тесты для класса Validator"""
    def test_validate_report_type_valid(self):
        """Тест корректных типов отчета"""
        assert Validator.validate_report_type('performance') == "performance"
        assert Validator.validate_report_type('table') == "table"
        assert Validator.validate_report_type('csv') == "csv"

    def test_validate_report_type_invalid(self):
        """Тест не корректных типов отчета"""
        with pytest.raises(argparse.ArgumentTypeError):
            Validator.validate_report_type('invalid_type')
        with pytest.raises(argparse.ArgumentTypeError):
            Validator.validate_report_type('excel')

    def test_validate_file_paths_all_valid(self):
        """Тест когда все файлы корректные"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f1:
            f1_path = f1.name
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f2:
            f2_path = f2.name
        try:
            files = [f1_path, f2_path]
            res = Validator.validate_file_paths(files)
            assert res == files
            assert len(res) == 2
        finally:
            os.unlink(f1_path)
            os.unlink(f2_path)

    def test_validate_file_paths_mixed(self):
        """Тест когда часть файлов не корректна"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            valid_file = f.name
        try:
            files = [valid_file, 'nonexistent.csv', 'file.txt']
            res = Validator.validate_file_paths(files)
            assert res == [valid_file]
            assert len(res) == 1
        finally:
            os.unlink(valid_file)

    def test_validate_file_paths_all_invalid(self):
        """Тест когда все файлы не корректные"""
        files = ['nonexistent.csv', 'file.txt', 'img.png']
        with pytest.raises(argparse.ArgumentTypeError):
            Validator.validate_report_type(files)