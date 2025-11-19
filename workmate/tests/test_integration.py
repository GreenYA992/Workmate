import csv
import os
import tempfile

# noinspection PyTypeChecker
from main import DataReader, EmpAnalyzer, ReportGen


class TestIntegration:
    def test_workflow(self, capsys):
        """Полный тест workflow"""
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
