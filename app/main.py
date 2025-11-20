import sys
from parser import main

if __name__ == "__main__":
    files = [
        "C://Users//Green//OneDrive//Рабочий стол//Обучение//ТЗ//workmate/"
        "/data_folder//employees1.csv",
        "C://Users//Green//OneDrive//Рабочий стол//Обучение//ТЗ//workmate/"
        "/data_folder//employees2.csv",
    ]
    sys.argv = (
        ["parser.py", "--files"]
        + files
        + ["--report", "table", "csv", "--output", "new_report.csv"]
    )

    main()
