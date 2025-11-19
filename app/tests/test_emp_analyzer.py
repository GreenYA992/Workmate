# noinspection PyTypeChecker
from parser import EmpAnalyzer


class TestEmpAnalyzer:
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
        """ТЕст на пустых данных"""
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
        pass
