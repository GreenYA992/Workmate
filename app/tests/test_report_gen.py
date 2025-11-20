"""Тест для модуля ReportGen"""

# noinspection PyTypeChecker
from parser import ReportGen


class TestReportGen:
    """Тестирование класса ReportGen"""

    def test_report_output(self, capsys):
        """Тест вывода отчета performance"""
        stats = [
            {"position": "Developer", "avg_performance": 4.75, "employee_count": 2},
            {"position": "QA", "avg_performance": 4.1, "employee_count": 1},
        ]

        ReportGen.report(stats)

        captured = capsys.readouterr()
        output = captured.out

        assert "Developer" in output and "4.75" in output
        assert "QA" in output and "4.10" in output
        assert "1" in output and "2" in output

        lines = output.strip().split("\n")
        assert len(lines) >= 4  # заголовок, разделитель и 2 строки

    def test_table_report(self, capsys):
        """Тест табличного отчета"""
        stats = [
            {"position": "Developer", "avg_performance": 4.75, "employee_count": 2},
        ]

        ReportGen.table_report(stats)
        captured = capsys.readouterr()
        output = captured.out

        assert "Должность" in output
        assert "Рейтинг" in output
        assert "Developer" in output
        assert "4.75" in output
