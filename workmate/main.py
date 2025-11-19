from parser import main
import sys

if __name__ == "__main__":
    files = [
        'C://Users//Green//OneDrive//Рабочий стол//Обучение//ТЗ//workmate//employees1.csv',
        'C://Users//Green//OneDrive//Рабочий стол//Обучение//ТЗ//workmate//employees2.csv',
    ]
    sys.argv = (['parser.py', '--files']
                + files +
                ['--report', 'table', 'csv', '--output', 'new_report.csv'])

    main()