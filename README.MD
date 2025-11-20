# Employee Performance Analyzer

Скрипт для анализа эффективности сотрудников на основе CSV-файлов. 
Формирует отчет с рейтингом должностей по среднему показателю performance.

## Установка

```bash
pip install -r requirements.txt

```

Использование

-- Командная строка (из директории app)
```bash
python parser.py --files ../data_folder/employees1.csv ../data_folder/employees2.csv --report performance

```

-- Альтернатива, можно прописать параметры запуска в main
(Стартовые параметры установлены).
Можно поменять параметры:

Параметр --report варианты "performance", "table", "csv"

Дополнительный параметр --output (по желанию, можно указать название файла CSV)
по умолчанию (без этого параметра) будет report.csv

В список files можно прописать пути к файлам, для обработки

```bash
python main.py

```

-- Запуск тестов
```bash
pytest

```

-- Пример запуска скрипта (performance вывод)

    position               performance
--  -------------------  -------------
 1  Backend Developer             4.83
 2  DevOps Engineer               4.80
 3  Data Engineer                 4.70
 4  Fullstack Developer           4.70
 5  Frontend Developer            4.65
 6  Data Scientist                4.65
 7  Mobile Developer              4.60
 8  QA Engineer                   4.50



