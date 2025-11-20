import subprocess
import sys


def test_cli_nonexistent_files():
    """
    Тест CLI с несуществующими данными.
    Пользовательский путь

    """
    res = subprocess.run(
        [
            sys.executable,
            "parser.py",
            "--files",
            "nonexistent.csv",
            "--report",
            "performance",
        ],
        capture_output=True,
        text=True,
    )

    # Должен завершиться с ошибкой
    assert res.returncode != 0

    combined_output = res.stdout + res.stderr
    assert "не найдено" in combined_output.lower()
