# noinspection PyTypeChecker
from parser import ReportGen


class TestReportGen:
    def test_report_output(self, capsys):
        """Тест вывода отчета performance"""
        stats = [
            {"position": "Developer", "avg_performance": 4.75, "employee_count": 2},
            {"position": "QA", "avg_performance": 4.1, "employee_count": 1},
        ]

        ReportGen.report(stats)

        captured = capsys.readouterr()
        output = captured.out

        assert "1 Developer 4.75" in output
        assert "2 QA 4.1" in output
        assert output.strip().count("\n") == 1

    def test_table_report(self, capsys):
        """Тест табличного отчета"""
        stats = [
            {"position": "Developer", "avg_performance": 4.75, "employee_count": 2},
        ]

        ReportGen.table_report(stats, 1)
        captured = capsys.readouterr()
        output = captured.out

        assert "Должность" in output
        assert "Рейтинг" in output
        assert "Developer" in output
        assert "4.75" in output
