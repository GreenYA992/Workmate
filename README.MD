# Employee Performance Analyzer

Скрипт для анализа эффективности сотрудников на основе CSV-файлов. 
Формирует отчет с рейтингом должностей по среднему показателю performance.

## Установка

```bash
pip install -r requirements.txt

```

Использование

-- Командная строка
```bash
python parser.py --files employees1.csv employees2.csv --report performance

```

-- Альтернатива, можно прописать параметры запуска в main
(Стартовые параметры установлены)
```bash
python main.py 

```

-- Запуск тестов
```bash
pytest

```


